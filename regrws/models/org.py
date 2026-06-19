from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import HttpUrl
from pydantic_xml import element, wrapped

from regrws.api.manager import BaseManager
from regrws.models.base import NSMAP, BaseModel
from regrws.models.poc import PocLinkRef
from regrws.models.tickets import Ticket

from regrws.models.nested import Iso31661, MultiLineElement
from regrws.models.types import iso3166_2_type


class OrgManager(BaseManager):
    def create(self, return_type=Ticket, *args, **kwargs):
        return super().create(return_type, *args, **kwargs)


class Org(BaseModel, tag="org", nsmap=NSMAP, search_mode="unordered"):
    iso3166_1: Iso31661
    street_address: List[MultiLineElement] = wrapped(
        "streetAddress", element(tag="line")
    )
    city: str = element()
    iso3166_2: Optional[iso3166_2_type] = element(tag="iso3166-2", default=None)
    postal_code: Optional[str] = element(tag="postalCode", default=None)

    comment: Optional[List[MultiLineElement]] = wrapped(
        "comment", element(tag="line"), default=None
    )

    handle: Optional[str] = element(default=None)
    registration_date: Optional[str] = element(tag="registrationDate", default=None)

    org_name: str = element(tag="orgName")
    dba_name: Optional[str] = element(tag="dbaName", default=None)
    tax_id: Optional[str] = element(tag="taxId", default=None)
    org_url: Optional[HttpUrl] = element(tag="orgUrl", default=None)

    poc_links: List[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))

    _endpoint: ClassVar[str] = "/org"
    _manager_class: ClassVar[type[BaseManager]] = OrgManager
