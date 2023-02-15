"""Net Model"""
from typing import ClassVar, List, Literal, Optional

from pydantic import root_validator
from pydantic_xml.model import element, wrapped

from regrws.api.manager import BaseManager

from .base import NSMAP, BaseModel
from .nested import IPVersionEnum, MultiLineElement, OriginAS
from .poc import PocLinkRef
from .types import ZeroPaddedIPvAnyAddress, cidr_length_type


class NetManager(BaseManager):
    """Custom Manager for Net Payloads"""

    def create(self, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover


class NetBlock(BaseModel, tag="netBlock", nsmap=NSMAP):
    type: Literal[
        "A",
        "AF",
        "AP",
        "AR",
        "AV",
        "DA",
        "FX",
        "IR",
        "IU",
        "LN",
        "LX",
        "PV",
        "PX",
        "RD",
        "RN",
        "RV",
        "RX",
        "S",
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


class Net(BaseModel, tag="net", nsmap=NSMAP):
    version: IPVersionEnum = element()
    comment: Optional[List[MultiLineElement]] = wrapped("comment", element(tag="line"))

    org_handle: Optional[str] = element(tag="orgHandle")
    customer_handle: Optional[str] = element(tag="customerHandle")

    handle: Optional[str] = element()
    registration_date: Optional[str] = element(tag="registrationDate")

    net_name: Optional[str] = element(tag="netName")
    net_blocks: Optional[List[NetBlock]] = wrapped("netBlocks", element(tag="netBlock"))

    parent_net_handle: Optional[str] = element(tag="parentNetHandle")

    origin_ases: Optional[List[OriginAS]] = wrapped(
        "originASes", element(tag="originAS", default_factory=list)
    )

    poc_links: List[PocLinkRef] = wrapped("pocLinks", element(tag="pocLinkRef"))

    _endpoint: ClassVar[str] = "/net"
    _manager: ClassVar[type[BaseManager]] = NetManager

    @root_validator(pre=True)
    def check_related_handle(cls, values):
        results = values.get("org_handle"), values.get("customer_handle")
        results_are_none = map(lambda x: x is None, results)
        if all(results_are_none):
            raise ValueError(
                "either `org_handle` or `customer_handle` must be provided"
            )
        if all(results):
            raise ValueError(
                "`orgHandle` and `customerHandle` elements are mutually exclusive."
            )
        return values
