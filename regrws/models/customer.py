"""Customer Model"""

from __future__ import annotations

from typing import ClassVar, List

from pydantic_xml.model import element, wrapped


from regrws.models.nested import Iso31661, MultiLineElement
from regrws.models.net import Net
from regrws.models.types import iso3166_2_type

from regrws.models.base import NSMAP, BaseManager, BaseModel


class CustomerManager(BaseManager):
    """Custom Manager for Customer Payloads"""

    def create(self, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def create_for_net(self, net: Net, *args, **kwargs) -> Customer | None:
        """
        https://www.arin.net/resources/manage/regrws/methods/#create-recipient-customer
        """
        instance = self.model(*args, **kwargs)
        instance.manager = self
        url = net.absolute_url
        if url:
            url = url + "/customer"
            return self._do(
                "post",
                url,
                instance.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore
            )
        return None  # pragma: no cover


class Customer(BaseModel, tag="customer", nsmap=NSMAP, search_mode="unordered"):
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
    _manager_class: ClassVar[type[BaseManager]] = CustomerManager
