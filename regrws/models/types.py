from ipaddress import IPv4Address, IPv6Address
from typing import Union

from pydantic import IPvAnyAddress
from pydantic.errors import IPvAnyAddressError
from pydantic_xml.model import BaseXmlModel

from .base import BaseModel

XmlModelType = type[BaseModel] | type[BaseXmlModel] | BaseModel | BaseXmlModel


class ZeroPaddedIPvAnyAddress(IPvAnyAddress):
    __slots__ = ()

    @classmethod
    def validate(cls, value: Union[str, bytes, int]) -> Union[IPv4Address, IPv6Address]:
        try:
            return IPv6Address(value)
        except ValueError:
            pass

        try:
            return IPv4Address(value)
        except ValueError:
            pass

        try:
            host_bytes = value.split(".")
            valid_bytes = [int(b) for b in host_bytes]
            valid = [str(b) for b in valid_bytes if b >= 0 and b <= 255]
            if len(host_bytes) == 4 and len(valid) == 4:
                return IPv4Address(".".join(valid))
            raise IPvAnyAddressError()
        except ValueError:
            raise IPvAnyAddressError()