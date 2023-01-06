from typing import List, Optional, Literal
from pydantic_xml import BaseXmlModel, attr, element, wrapped
from pydantic import HttpUrl, constr
from enum import IntEnum

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
    name: str = element()  # type: ignore
    code2: constr(min_length=2, max_length=2, to_upper=True) = element()  # type: ignore
    code3: constr(min_length=3, max_length=3, to_upper=True) = element()  # type: ignore
    e164: int = element()  # type: ignore


class MultiLineElement(BaseXmlModel):
    number: int = attr()  # type: ignore
    line: str


class PocLinkRef(BaseXmlModel, tag="pocLinkRef", nsmap=NSMAP):
    description: Literal["Admin", "Tech", "Routing"] = attr()  # type: ignore
    function: Literal["AD", "T", "R"] = attr()  # type: ignore
    handle: str = attr()  # type: ignore


class Org(BaseXmlModel, tag="org", nsmap=NSMAP):
    iso3166_1: Iso3166_1  # type: ignore
    street_address: List[MultiLineElement] = wrapped("streetAddress", element(tag="line"))  # type: ignore
    city: str = element()  # type: ignore
    iso3166_2: Optional[constr(max_length=3, to_upper=True)] = element(tag="iso3166-2")  # type: ignore
    postal_code: Optional[str] = element(tag="postalCode")  # type: ignore
    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))  # type: ignore

    handle: Optional[str] = element()  # type: ignore
    registration_date: Optional[str] = element(tag="registrationDate")  # type: ignore
    org_name: str = element(tag="orgName")  # type: ignore
    dba_name: Optional[str] = element(tag="dbaName")  # type: ignore
    tax_id: Optional[str] = element(tag="taxId")  # type: ignore
    org_url: Optional[HttpUrl] = element(tag="orgUrl")  # type: ignore

    poc_links: List[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))  # type: ignore


class Customer(BaseXmlModel, tag="customer", nsmap=NSMAP):
    customer_name: str = element(tag="customerName")  # type: ignore
    iso3166_1: Iso3166_1  # type: ignore
    street_address: List[MultiLineElement] = wrapped("streetAddress", element(tag="line"))  # type: ignore
    city: str = element()  # type: ignore
    iso3166_2: Optional[constr(max_length=3, to_upper=True)] = element(tag="iso3166-2")  # type: ignore
    postal_code: Optional[str] = element(tag="postalCode")  # type: ignore
    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))  # type: ignore

    handle: Optional[str] = element()  # type: ignore
    parent_org_handle: Optional[str] = element(tag="parentOrgHandle")  # type: ignore

    registration_date: Optional[str] = element(tag="registrationDate")  # type: ignore
    private_customer: Optional[bool] = element(tag="privateCustomer")  # type: ignore
