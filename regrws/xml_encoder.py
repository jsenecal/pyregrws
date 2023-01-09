import ipaddress
from typing import Any

from pydantic_xml import XmlEncoder


class IPaddressXmlEncoder(XmlEncoder):
    def encode(self, obj: Any) -> str:
        if isinstance(obj, (ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, ipaddress.IPv6Network)):
            return str(obj)
        return super().encode(obj)