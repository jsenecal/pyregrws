from ipaddress import IPv4Address, IPv6Address
from typing import Union

from pydantic import Field, StringConstraints
from pydantic_core import PydanticCustomError
from pydantic.networks import IPvAnyAddress
from pydantic_xml.model import BaseXmlModel

from regrws.models.base import BaseModel
from typing_extensions import Annotated

xmlmodel_type = type[BaseModel] | type[BaseXmlModel] | BaseModel | BaseXmlModel


code2_type = Annotated[str, StringConstraints(min_length=2, max_length=2, to_upper=True)]
code3_type = Annotated[str, StringConstraints(min_length=3, max_length=3, to_upper=True)]
iso3166_2_type = Annotated[str, StringConstraints(max_length=3, to_upper=True)]
cidr_length_type = Annotated[int, Field(ge=0, le=128)]


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
            raise PydanticCustomError('ip_any_address', 'value is not a valid IPv4 or IPv6 address')  # pragma: no cover

        except ValueError:  # pragma: no cover
            raise PydanticCustomError('ip_any_address', 'value is not a valid IPv4 or IPv6 address')
