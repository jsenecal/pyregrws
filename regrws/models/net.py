"""Net Model"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, List, Literal, Optional

from pydantic import root_validator
from pydantic_xml.model import element, wrapped

from regrws.api.manager import BaseManager

from regrws.models.base import NSMAP, BaseModel
from regrws.models.nested import IPVersionEnum, MultiLineElement, OriginAS
from regrws.models.poc import PocLinkRef
from regrws.models.types import ZeroPaddedIPvAnyAddress, cidr_length_type

if TYPE_CHECKING:
    from regrws.models.tickets import TicketRequest


class NetManager(BaseManager):
    """Custom Manager for Net Payloads"""

    def create(self, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def delete(self, instance: type[BaseModel], return_type=None):
        """This call will generate an automatically-processed ticketed request to delete the NET"""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        return super().delete(instance, TicketRequest)

    def remove(self, instance: type[Net]) -> TicketRequest | None:
        """This call will remove the network from the ARIN database. It is only applicable for reallocations or reassignments.
        It differs from the Delete NET call in that attachments can be sent using the NET payload."""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        url = instance.absolute_url
        if url:
            url = str(url) + "/remove"
            return self._do(
                "put",
                url,
                data=instance.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore
                return_type=TicketRequest,
            )
        return None  # pragma: no cover

    def reassign(self, instance: type[Net], net: type[Net]) -> TicketRequest | None:
        """This call performs a reassignment from the NET instance using the recipient information from the object."""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        url = instance.absolute_url
        if url:
            url = str(url) + "/reassign"
            return self._do(
                "put",
                url,
                data=net.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore
                return_type=TicketRequest,
            )
        return None  # pragma: no cover

    def reallocate(self, instance: type[Net], net: type[Net]) -> TicketRequest | None:
        """This call performs a reallocation from the NET instance using the recipient information from the object."""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        url = instance.absolute_url
        if url:
            url = str(url) + "/reallocate"
            return self._do(
                "put",
                url,
                data=net.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore
                return_type=TicketRequest,
            )
        return None  # pragma: no cover

    def find_parent(
        self,
        start_address: ZeroPaddedIPvAnyAddress,
        end_address: ZeroPaddedIPvAnyAddress,
    ) -> Net | None:
        """This call finds the parent of the network represented by the start and end IP range and returns a NET payload containing the details of the parent NET."""
        if self.model._endpoint:
            url = f"{self.api.base_url}{self.model._endpoint}/parentNet/{start_address}/{end_address}"
            return self._do("get", url)  # type: ignore
        return None  # pragma: no cover

    def find_net(
        self,
        start_address: ZeroPaddedIPvAnyAddress,
        end_address: ZeroPaddedIPvAnyAddress,
    ) -> Net | None:
        """This call finds the network details related to the start and end IP range.
        If multiple networks exist for the same IP range, then the most specific network is returned."""
        if self.model._endpoint:
            url = f"{self.api.base_url}{self.model._endpoint}/mostSpecificNet/{start_address}/{end_address}"
            return self._do("get", url)  # type: ignore
        return None  # pragma: no cover


class NetBlock(BaseModel, tag="netBlock", nsmap=NSMAP, search_mode="unordered"):
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
    def check_payload(cls, values):  # pragma: no cover
        results = values.get("end_address") is None, values.get("cidr_length") is None
        if all(results):
            raise ValueError("either `end_address` or `cidr_length` must be provided")
        return values


class Net(BaseModel, tag="net", nsmap=NSMAP, search_mode="unordered"):
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
    _manager_class: ClassVar[type[BaseManager]] = NetManager

    @root_validator(pre=True)
    def check_related_handle(cls, values):  # pragma: no cover
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

    def remove(self) -> TicketRequest | None:
        """Remove the Net from the ARIN database"""
        if self._manager is None:
            return None  # pragma: no cover
        return self._manager.remove(self)

    def reassign(self, net: type[Net]) -> TicketRequest | None:
        """Reassign the child Net to a different Org or Customer"""
        if self._manager is None:
            return None  # pragma: no cover
        return self._manager.reassign(self, net)

    def reallocate(self, net: type[Net]) -> TicketRequest | None:
        """Reallocate the child Net to a different Org or Customer"""
        if self._manager is None:
            return None  # pragma: no cover
        return self._manager.reallocate(self, net)
