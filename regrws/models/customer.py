from __future__ import annotations

from typing import ClassVar, List, TYPE_CHECKING

from pydantic_xml.model import element, wrapped

from regrws.models.nested import Iso31661, MultiLineElement
from regrws.models.types import iso3166_2_type

from .base import NSMAP, BaseManager, BaseModel


class CustomerManager(BaseManager):
    """Custom Manager for Customer Payloads"""

    def create(self, *args, **kwargs):
        """
        https://www.arin.net/resources/manage/regrws/methods/#create-recipient-customer
        """
        raise NotImplementedError  # pragma: no cover


class Customer(BaseModel, tag="customer", nsmap=NSMAP):
    """
    https://www.arin.net/resources/manage/regrws/payloads/#customer-payload
    """

    customer_name: str = element(tag="customerName")

    iso3166_1: Iso31661
    street_address: List[MultiLineElement] = wrapped(
        "streetAddress", element(tag="line")
    )
    city: str = element()
    iso3166_2: iso3166_2_type | None = element(tag="iso3166-2")
    postal_code: str | None = element(tag="postalCode")

    comment: List[MultiLineElement] | None = wrapped("comment", element(tag="line"))

    handle: str | None = element()
    parent_org_handle: str | None = element(tag="parentOrgHandle")
    registration_date: str | None = element(tag="registrationDate")

    private_customer: bool | None = element(tag="privateCustomer")

    _endpoint: ClassVar[str] = "/customer"
    _manager_class = CustomerManager
