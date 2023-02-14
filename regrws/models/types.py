from ipaddress import IPv4Address, IPv6Address
from typing import Union

from pydantic import conint, constr
from pydantic.errors import IPvAnyAddressError
from pydantic.networks import IPvAnyAddress
from pydantic_xml.model import BaseXmlModel

from .base import BaseModel

xmlmodel_type = type[BaseModel] | type[BaseXmlModel] | BaseModel | BaseXmlModel


code2_type = constr(min_length=2, max_length=2, to_upper=True)
code3_type = constr(min_length=3, max_length=3, to_upper=True)
iso3166_2_type = constr(max_length=3, to_upper=True)
cidr_length_type = conint(ge=0, le=128)


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
