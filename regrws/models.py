from __future__ import annotations
from typing import List, Optional, Literal
from pydantic_xml import BaseXmlModel, attr, element, wrapped
from pydantic import HttpUrl, constr, conint, IPvAnyAddress
from enum import IntEnum

from .types import ZeroPaddedIPvAnyAddress

# types
code2_type = constr(min_length=2, max_length=2, to_upper=True)
code3_type = constr(min_length=3, max_length=3, to_upper=True)
iso3166_2_type = constr(max_length=3, to_upper=True)
cidr_length_type = conint(ge=0, le=128)

NSMAP = {"": "http://www.arin.net/regrws/core/v1"}


ALGORITHM_NAMES_MAP = {
    5: "RSA/SHA-1",
    7: "RSASHA1-NSEC3-SHA1",
    8: "RSA/SHA-256",
    10: "RSA/SHA-512",
    13: "ECDSA Curve P-256 with SHA-256",
    14: "ECDSA Curve P-384 with SHA-384",
}


class AlgorithmEnum(IntEnum):
    SHA1 = 5
    NSEC3SHA1 = 7
    SHA256 = 8
    SHA512 = 10
    ECDSA256 = 13
    ECDSA384 = 14


class Iso3166_1(BaseXmlModel, tag="iso3166-1", nsmap=NSMAP):
    name: str = element()
    code2: code2_type = element()
    code3: code3_type = element()
    e164: int = element()


class MultiLineElement(BaseXmlModel):
    number: int = attr()
    line: str


class PocLinkRef(BaseXmlModel, tag="pocLinkRef", nsmap=NSMAP):
    description: Literal["Admin", "Tech", "Routing"] = attr()
    function: Literal["AD", "T", "R"] = attr()
    handle: str = attr()


class Org(BaseXmlModel, tag="org", nsmap=NSMAP):
    iso3166_1: Iso3166_1
    street_address: List[MultiLineElement] = wrapped("streetAddress", element(tag="line"))
    city: str = element()
    iso3166_2: Optional[iso3166_2_type] = element(tag="iso3166-2")
    postal_code: Optional[str] = element(tag="postalCode")

    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))

    handle: Optional[str] = element()
    registration_date: Optional[str] = element(tag="registrationDate")

    org_name: str = element(tag="orgName")
    dba_name: Optional[str] = element(tag="dbaName")
    tax_id: Optional[str] = element(tag="taxId")
    org_url: Optional[HttpUrl] = element(tag="orgUrl")

    poc_links: List[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))


class Customer(BaseXmlModel, tag="customer", nsmap=NSMAP):
    customer_name: str = element(tag="customerName")

    iso3166_1: Iso3166_1
    street_address: List[MultiLineElement] = wrapped("streetAddress", element(tag="line"))
    city: str = element()
    iso3166_2: Optional[iso3166_2_type] = element(tag="iso3166-2")
    postal_code: Optional[str] = element(tag="postalCode")

    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))

    handle: Optional[str] = element()
    parent_org_handle: Optional[str] = element(tag="parentOrgHandle")
    registration_date: Optional[str] = element(tag="registrationDate")

    private_customer: Optional[bool] = element(tag="privateCustomer")

class NetBlock(BaseXmlModel, tag="netBlock", nsmap=NSMAP):
    type: Literal["A", "AF", "AP", "AR", "AV", "DA", "FX", "IR", "IU", "LN", "LX", "PV", "PX", "RD", "RN", "RV", "RX", "S"] = element()
    description: Optional[str] = element()
    start_address: ZeroPaddedIPvAnyAddress  = element(tag="startAddress") 
    end_address: ZeroPaddedIPvAnyAddress  = element(tag="endAddress")
    cidr_length: cidr_length_type = element(tag="cidrLength")