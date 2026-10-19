from __future__ import annotations

from typing import ClassVar

from pydantic import HttpUrl
from pydantic_xml import element, wrapped

from regrws.api.manager import BaseManager
from regrws.models.base import NSMAP, BaseModel
from regrws.models.nested import Iso31661, MultiLineElement
from regrws.models.poc import PocLinkRef
from regrws.models.tickets import Ticket
from regrws.models.types import iso3166_2_type


class OrgManager(BaseManager):
    def create(self, return_type=Ticket, *args, **kwargs):
        return super().create(return_type, *args, **kwargs)


class Org(BaseModel, tag="org", nsmap=NSMAP, search_mode="unordered"):
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

    org_name: str = element(tag="orgName")
    dba_name: str | None = element(tag="dbaName", default=None)
    tax_id: str | None = element(tag="taxId", default=None)
    org_url: HttpUrl | None = element(tag="orgUrl", default=None)

    poc_links: list[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))

    _endpoint: ClassVar[str] = "/org"
    _manager_class: ClassVar[type[BaseManager]] = OrgManager
