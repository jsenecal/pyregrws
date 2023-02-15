from enum import IntEnum
from typing import Literal

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


class Iso31661(BaseModel, tag="iso3166-1", nsmap=NSMAP):
    name: str = element()
    code2: code2_type = element()
    code3: code3_type = element()
    e164: int = element()


class MultiLineElement(BaseModel):
    number: int = attr()
    line: str


class Attachment(BaseModel, tag="attachment", nsmap=NSMAP):
    data: str = element()
    filename: str = element()


class PhoneType(BaseModel, tag="type", nsmap=NSMAP):
    description: str = element()
    code: Literal["O", "M", "F"] = element()


class Phone(BaseModel, tag="phone", nsmap=NSMAP):
    type: PhoneType = element()
    number: str = element()
    extension: str | None = element()


class OriginAS(BaseModel, tag="originAS", nsmap=NSMAP):
    asn: str
