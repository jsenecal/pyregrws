from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Union

from pydantic import Field
from pydantic.functional_validators import BeforeValidator
from pydantic_xml import BaseXmlModel

from regrws.models.base import BaseModel

xmlmodel_type = type[BaseModel] | type[BaseXmlModel] | BaseModel | BaseXmlModel


def _to_upper(v: str) -> str:
    """Convert string to uppercase."""
    return v.upper() if isinstance(v, str) else v


code2_type = Annotated[
    str, Field(min_length=2, max_length=2), BeforeValidator(_to_upper)
]
code3_type = Annotated[
    str, Field(min_length=3, max_length=3), BeforeValidator(_to_upper)
]
iso3166_2_type = Annotated[str, Field(max_length=3), BeforeValidator(_to_upper)]
cidr_length_type = Annotated[int, Field(ge=0, le=128)]


def _validate_ip_address(
    value: Union[str, bytes, int],
) -> Union[IPv4Address, IPv6Address]:
    """Validate IP addresses, supporting both IPv4 and IPv6.

    ARIN returns zero-padded octets (e.g., 010.000.000.001) which Python 3.11+
    rejects due to octal ambiguity. We strip the padding before parsing.
    """
    try:
        return IPv6Address(value)
    except ValueError:
        pass

    try:
        return IPv4Address(value)
    except ValueError:
        pass

    # Handle zero-padded IPv4 addresses from ARIN
    if isinstance(value, str) and "." in value:
        octets = value.split(".")
        if len(octets) == 4:
            try:
                # Strip leading zeros and validate each octet
                stripped = [str(int(o)) for o in octets]
                return IPv4Address(".".join(stripped))
            except ValueError:
                pass

    raise ValueError(f"Invalid IP address: {value}")


ZeroPaddedIPvAnyAddress = Annotated[
    Union[IPv4Address, IPv6Address],
    BeforeValidator(_validate_ip_address),
]
