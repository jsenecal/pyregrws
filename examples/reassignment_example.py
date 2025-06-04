#!/usr/bin/env python3
"""
ARIN IP Reassignment/Reallocation Example

This example demonstrates how to use the pyregrws library to perform IP network
reassignments and reallocations with ARIN's Reg-RWS API.

This script shows how to:
1. Find existing ARIN network records
2. Create customer records for reassignments
3. Perform network reassignments using the "Reassign Simple" method
4. Handle error cases and validation

Requirements:
- ARIN API key (set as environment variable ARIN_API_KEY)
- IP networks that you have authority to reassign
"""

import os
import sys
from ipaddress import IPv4Network, IPv6Network, ip_network
from typing import Union, Optional, Literal
from dataclasses import dataclass

from regrws.api.core import Api
from regrws.models import Customer, Error, Net
from regrws.models.nested import IPVersionEnum, Iso31661, MultiLineElement
from regrws.models.net import NetBlock


@dataclass
class CustomerInfo:
    """Information needed to create a customer for reassignment"""
    name: str
    street_address: str
    city: str
    state_province: str  # ISO 3166-2 code (e.g., "CA", "TX")
    postal_code: str
    country: str = "United States"


class ARINReassignmentTool:
    """Tool for performing ARIN IP network reassignments"""
    
    def __init__(self, api_key: str, base_url: str = "https://reg.arin.net/rws"):
        """
        Initialize the ARIN reassignment tool
        
        Args:
            api_key: Your ARIN API key
            base_url: ARIN API base URL (production or test)
        """
        self.api = Api(api_key=api_key, base_url=base_url)
        self.countries = {
            "Canada": Iso31661(name="Canada", code2="CA", code3="CAN", e164=1),
            "United States": Iso31661(name="United States of America", code2="US", code3="USA", e164=1),
        }
    
    def find_network(self, network: Union[IPv4Network, IPv6Network]) -> Optional[Net]:
        """
        Find an existing ARIN network record for the given IP network
        
        Args:
            network: IP network to search for
            
        Returns:
            Net object if found, None otherwise
        """
        print(f"Searching for ARIN network record for {network}")
        
        if network.prefixlen == 31:
            # Special case for /31 networks
            result = self.api.net.find_net(network.network_address, network.network_address + 1)
        else:
            result = self.api.net.find_net(network.network_address, network.broadcast_address)
        
        if isinstance(result, Error):
            if result.code == "E_OBJECT_NOT_FOUND":
                print(f"No ARIN network found for {network}")
                return None
            else:
                print(f"Error searching for network {network}: {result}")
                return None
        elif result is None:
            print(f"Unable to process ARIN response for {network}")
            return None
        else:
            print(f"Found ARIN network: {result.handle} ({result.net_name})")
            return result
    
    def create_customer(self, customer_info: CustomerInfo, parent_net: Net) -> Optional[Customer]:
        """
        Create a customer record for reassignment
        
        Args:
            customer_info: Customer information
            parent_net: Parent network for the customer creation
            
        Returns:
            Customer object if successful, None otherwise
        """
        print(f"Creating customer record for {customer_info.name}")
        
        # Get country information
        if customer_info.country not in self.countries:
            print(f"Unsupported country: {customer_info.country}")
            return None
        
        iso3166_1 = self.countries[customer_info.country]
        
        # Create street address
        street_address = [MultiLineElement(number=1, line=customer_info.street_address)]
        
        # Create customer object
        customer = Customer(
            customer_name=customer_info.name,
            iso3166_1=iso3166_1,
            street_address=street_address,
            city=customer_info.city,
            iso3166_2=customer_info.state_province,
            postal_code=customer_info.postal_code,
            private_customer=False,
            comments=[MultiLineElement(number=1, line="Created via pyregrws example")]
        )
        
        # Create customer via ARIN API
        result = self.api.customer.create_for_net(parent_net, **customer.dict())
        
        if isinstance(result, Error):
            print(f"Error creating customer: {result}")
            return None
        elif result is None:
            print("Unable to process ARIN response for customer creation")
            return None
        else:
            print(f"Created customer: {result.handle}")
            return result
    
    def create_netblock(
        self, 
        network: Union[IPv4Network, IPv6Network],
        block_type: Literal["A", "AF", "AP", "AR", "AV", "DA", "FX", "IR", "IU", 
                           "LN", "LX", "PV", "PX", "RD", "RN", "RV", "RX", "S"] = "S"
    ) -> NetBlock:
        """
        Create a NetBlock object from an IP network
        
        Args:
            network: IP network
            block_type: Type of network block (S = Simple reassignment)
            
        Returns:
            NetBlock object
        """
        return NetBlock(
            start_address=network.network_address,
            end_address=None,  # ARIN will calculate this
            cidr_length=network.prefixlen,
            type=block_type
        )
    
    def generate_net_name(self, network: Union[IPv4Network, IPv6Network], customer_name: str) -> str:
        """
        Generate a network name for the reassignment
        
        Args:
            network: IP network
            customer_name: Customer name
            
        Returns:
            Generated network name
        """
        network_str = str(network).replace(".", "-").replace("/", "-").replace(":", "-")
        customer_slug = customer_name.upper().replace(" ", "-")[:20]  # Limit length
        return f"{customer_slug}-{network_str}"
    
    def create_reassignment_net(
        self,
        network: Union[IPv4Network, IPv6Network],
        parent_net: Net,
        customer_handle: str,
        net_name: Optional[str] = None
    ) -> Net:
        """
        Create a Net object for reassignment
        
        Args:
            network: IP network to reassign
            parent_net: Parent network
            customer_handle: Customer handle for the reassignment
            net_name: Optional network name (auto-generated if not provided)
            
        Returns:
            Net object ready for reassignment
        """
        version = IPVersionEnum(network.version)
        
        if net_name is None:
            net_name = f"REASSIGN-{str(network).replace('.', '-').replace('/', '-').replace(':', '-')}"
        
        net_block = self.create_netblock(network, "S")  # S = Simple reassignment
        
        return Net(
            version=version,
            net_name=net_name,
            net_blocks=[net_block],
            parent_net_handle=parent_net.handle,
            customer_handle=customer_handle,
            poc_links=[]  # POC links will be inherited from parent
        )
    
    def reassign_network(
        self,
        network: Union[IPv4Network, IPv6Network],
        customer_info: CustomerInfo,
        parent_net_handle: Optional[str] = None,
        dry_run: bool = False
    ) -> bool:
        """
        Perform a network reassignment
        
        Args:
            network: IP network to reassign
            customer_info: Customer information for the reassignment
            parent_net_handle: Optional parent network handle (will search if not provided)
            dry_run: If True, don't actually perform the reassignment
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'DRY RUN: ' if dry_run else ''}Starting reassignment of {network}")
        
        # Find parent network if not provided
        if parent_net_handle:
            parent_net = self.api.net.from_handle(parent_net_handle)
            if isinstance(parent_net, Error) or parent_net is None:
                print(f"Error retrieving parent network {parent_net_handle}")
                return False
        else:
            # Find the network or its parent
            parent_net = self.find_network(network)
            if parent_net is None:
                print(f"Could not find parent network for {network}")
                return False
        
        # Check if this exact network is already reassigned
        existing_net = self.find_network(network)
        if existing_net and existing_net.handle != parent_net.handle:
            if existing_net.customer_handle:
                print(f"Network {network} is already reassigned to customer {existing_net.customer_handle}")
                return True
            else:
                print(f"Network {network} exists but is not reassigned")
        
        if dry_run:
            print(f"DRY RUN: Would reassign {network} under parent {parent_net.handle}")
            return True
        
        # Create customer
        customer = self.create_customer(customer_info, parent_net)
        if customer is None:
            return False
        
        # Create reassignment network
        net_name = self.generate_net_name(network, customer_info.name)
        reassignment_net = self.create_reassignment_net(
            network, parent_net, customer.handle, net_name
        )
        
        # Perform the reassignment
        print(f"Performing reassignment of {network}")
        result = parent_net.reassign(reassignment_net)
        
        if isinstance(result, Error):
            print(f"Error performing reassignment: {result}")
            return False
        elif result is None:
            print("Unable to process ARIN response for reassignment")
            return False
        else:
            print(f"Successfully reassigned {network} to {result.net.handle}")
            return True


def main():
    """Example usage of the ARIN reassignment tool"""
    
    # Get API key from environment
    api_key = os.getenv("ARIN_API_KEY")
    if not api_key:
        print("Please set ARIN_API_KEY environment variable")
        sys.exit(1)
    
    # Use test environment for this example
    # Change to "https://reg.arin.net/rws" for production
    base_url = "https://reg.ote.arin.net/rws"  # Test environment
    
    # Initialize the tool
    tool = ARINReassignmentTool(api_key, base_url)
    
    # Example network to reassign (use your own network)
    network = ip_network("192.0.2.0/24")  # RFC 5737 documentation network
    
    # Customer information
    customer_info = CustomerInfo(
        name="Example Corporation",
        street_address="123 Main Street",
        city="Anytown",
        state_province="VA",  # Virginia
        postal_code="12345",
        country="United States"
    )
    
    # Perform reassignment (dry run first)
    print("=== DRY RUN ===")
    success = tool.reassign_network(network, customer_info, dry_run=True)
    
    if success:
        print("\n=== ACTUAL REASSIGNMENT ===")
        # Uncomment the next line to perform actual reassignment
        # success = tool.reassign_network(network, customer_info, dry_run=False)
        print("Actual reassignment commented out for safety")
    
    print(f"\nReassignment {'would succeed' if success else 'failed'}")


if __name__ == "__main__":
    main()