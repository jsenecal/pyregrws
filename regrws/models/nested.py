from enum import IntEnum
from typing import Literal, Optional

from pydantic import root_validator
from pydantic_xml.model import attr, element

from regrws.models.base import NSMAP, BaseModel
from regrws.models.types import code2_type, code3_type

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


class IPVersionEnum(IntEnum):
    IPV4 = 4
    IPV6 = 6


class Iso31661(BaseModel, tag="iso3166-1", nsmap=NSMAP, search_mode="unordered"):
    name: Optional[str] = element(default=None)
    code2: Optional[code2_type] = element(default=None)
    code3: Optional[code3_type] = element(default=None)
    e164: Optional[int] = element(default=None)

    @root_validator
    def require_code2_or_code3(cls, values):
        if values.get("code2") is None and values.get("code3") is None:
            raise ValueError("Either code2 or code3 must be specified")
        return values


class MultiLineElement(BaseModel):
    number: int = attr()
    line: str | None = ""


class Attachment(BaseModel, tag="attachment", nsmap=NSMAP, search_mode="unordered"):
    data: str = element()
    filename: str = element()


class PhoneType(BaseModel, tag="type", nsmap=NSMAP, search_mode="unordered"):
    description: str = element()
    code: Literal["O", "M", "F"] = element()


class Phone(BaseModel, tag="phone", nsmap=NSMAP, search_mode="unordered"):
    type: PhoneType = element()
    number: str = element()
    extension: str | None = element()


class OriginAS(BaseModel, tag="originAS", nsmap=NSMAP, search_mode="unordered"):
    asn: str
