from __future__ import annotations

from enum import IntEnum
from typing import List, Literal, Optional

from pydantic import HttpUrl, conint, constr, root_validator
from pydantic_xml.model import BaseXmlModel, attr, element, wrapped

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


class IPVersionEnum(IntEnum):
    IPV4 = 4
    IPV6 = 6


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
    type: Literal[
        "A", "AF", "AP", "AR", "AV", "DA", "FX", "IR", "IU", "LN", "LX", "PV", "PX", "RD", "RN", "RV", "RX", "S"
    ] = element()
    description: Optional[str] = element()
    start_address: ZeroPaddedIPvAnyAddress = element(tag="startAddress")
    end_address: Optional[ZeroPaddedIPvAnyAddress] = element(tag="endAddress")
    cidr_length: Optional[cidr_length_type] = element(tag="cidrLength")

    @root_validator(pre=True)
    def check_payload(cls, values):
        results = values.get("end_address") is None, values.get("cidr_length") is None
        if all(results):
            raise ValueError("either `end_address` or `cidr_length` must be provided")
        return values


class OriginAS(BaseXmlModel, tag="originAS", nsmap=NSMAP):
    asn: str


class Net(BaseXmlModel, tag="net", nsmap=NSMAP):
    version: IPVersionEnum = element()
    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))

    org_handle: Optional[str] = element(tag="orgHandle")
    customer_handle: Optional[str] = element(tag="customerHandle")

    handle: Optional[str] = element()
    registration_date: Optional[str] = element(tag="registrationDate")

    net_name: Optional[str] = element(tag="netName")
    net_blocks: Optional[List[NetBlock]] = wrapped("netBlocks", element(tag="netBlock"))

    parent_net_handle: Optional[str] = element(tag="parentNetHandle")

    origin_ases: Optional[List[OriginAS]] = wrapped("originASes", element(tag="originAS", default_factory=list))

    poc_links: List[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))

    @root_validator(pre=True)
    def check_related_handle(cls, values):
        results = values.get("org_handle"), values.get("customer_handle")
        results_are_none = map(lambda x: x is None, results)
        if all(results_are_none):
            raise ValueError("either `org_handle` or `customer_handle` must be provided")
        if all(results):
            raise ValueError("`org_handle` and `customer_handle` are mutually exclusive")
        return values


class ErrorComponent(BaseXmlModel, tag="component", nsmap=NSMAP):
    name: str = element()
    message: str = element()


class Error(BaseXmlModel, tag="error", nsmap=NSMAP):
    message: str = element()
    code: Literal[
        "E_SCHEMA_VALIDATION",
        "E_ENTITY_VALIDATION",
        "E_OBJECT_NOT_FOUND",
        "E_AUTHENTICATION",
        "E_NOT_REMOVEABLE",
        "E_BAD_REQUEST",
        "E_OUTAGE",
        "E_UNSPECIFIED",
    ] = element()
    components: List[ErrorComponent] = wrapped("components", element(tag="component"))
    additionnal_info: List[str] = wrapped("additionalInfo", element(tag="message", default_factory=list))
