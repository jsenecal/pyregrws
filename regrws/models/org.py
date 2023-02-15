from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic import HttpUrl
from pydantic_xml.model import element, wrapped

from regrws.api.manager import BaseManager
from regrws.models.base import NSMAP, BaseModel
from regrws.models.poc import PocLinkRef
from regrws.models.tickets import Ticket

from regrws.models.nested import Iso31661, MultiLineElement
from regrws.models.types import iso3166_2_type


class OrgManager(BaseManager):
    def create(self, return_type=Ticket, *args, **kwargs):
        return super().create(return_type, *args, **kwargs)


class Org(BaseModel, tag="org", nsmap=NSMAP):
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

    org_name: str = element(tag="orgName")
    dba_name: Optional[str] = element(tag="dbaName")
    tax_id: Optional[str] = element(tag="taxId")
    org_url: Optional[HttpUrl] = element(tag="orgUrl")

    poc_links: List[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))

    _endpoint: ClassVar[str] = "/org"
    _manager_class: ClassVar[type[BaseManager]] = OrgManager
