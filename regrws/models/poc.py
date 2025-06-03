from typing import ClassVar, List, Literal, Optional

from pydantic import root_validator
from pydantic_xml.model import attr, element, wrapped

from regrws.models.base import NSMAP, BaseModel
from regrws.models.nested import Iso31661, MultiLineElement, Phone
from regrws.models.types import iso3166_2_type


class PocLinkRef(BaseModel, tag="pocLinkRef", nsmap=NSMAP, search_mode="unordered"):
    description: Literal[
        "Abuse",
        "Admin",
        "NOC",
        "Routing",
        "Tech",
    ] = attr()
    function: Literal[
        "AB",
        "AD",
        "N",
        "R",
        "T",
    ] = attr()
    handle: str = attr()


class Poc(BaseModel, tag="poc", nsmap=NSMAP, search_mode="unordered"):
    iso3166_1: Iso31661
    street_address: List[MultiLineElement] = wrapped(
        "streetAddress", element(tag="line")
    )
    city: str = element()
    iso3166_2: Optional[iso3166_2_type] = element(tag="iso3166-2")
    postal_code: Optional[str] = element(tag="postalCode")

    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))

    handle: Optional[str] = element()
    registration_date: Optional[str] = element(tag="registrationDate")

    contact_type: Literal["PERSON", "ROLE"] = element(tag="contactType")

    company_name: Optional[str] = element(tag="companyName")

    first_name: Optional[str] = element(tag="firstName")
    middle_name: Optional[str] = element(tag="middleName")
    last_name: Optional[str] = element(tag="lastName")

    phones: List[Phone] = wrapped("phones", element(tag="phone"))

    _endpoint: ClassVar[str] = "/poc"

    @root_validator(pre=True)
    def check_contact_type_and_payload(cls, values):  # pragma: no cover
        contact_type = values.get("contact_type")

        if contact_type == "ROLE":
            msg = "this POC is a ROLE POC"
            if not values.get("company_name"):
                raise ValueError(msg + ", `company_name` is required")
            if not values.get("last_name"):
                raise ValueError(
                    msg + ", the role name must be entered in the 'last_name' field"
                )
            if values.get("first_name"):
                raise ValueError(msg + ", `first_name` must be left blank")
        return values
