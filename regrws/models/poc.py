from typing import Any, ClassVar, Literal

from pydantic import model_validator
from pydantic_xml import attr, element, wrapped

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
    street_address: list[MultiLineElement] = wrapped(
        "streetAddress", element(tag="line")
    )
    city: str = element()
    iso3166_2: iso3166_2_type | None = element(tag="iso3166-2", default=None)
    postal_code: str | None = element(tag="postalCode", default=None)

    comment: list[MultiLineElement] | None = wrapped(
        "comment", element(tag="line"), default=None
    )

    handle: str | None = element(default=None)
    registration_date: str | None = element(tag="registrationDate", default=None)

    contact_type: Literal["PERSON", "ROLE"] = element(tag="contactType")

    company_name: str | None = element(tag="companyName", default=None)

    first_name: str | None = element(tag="firstName", default=None)
    middle_name: str | None = element(tag="middleName", default=None)
    last_name: str | None = element(tag="lastName", default=None)

    emails: list[str] = wrapped("emails", element(tag="email"))

    phones: list[Phone] = wrapped("phones", element(tag="phone"))

    _endpoint: ClassVar[str] = "/poc"

    @model_validator(mode="before")
    @classmethod
    def check_contact_type_and_payload(cls, values: Any) -> Any:  # pragma: no cover
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
