"""Net Model"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Literal, NoReturn, cast

from pydantic import model_validator
from pydantic_xml import element, wrapped

from regrws.api.manager import BaseManager
from regrws.models.base import NSMAP, BaseModel
from regrws.models.nested import IPVersionEnum, MultiLineElement, OriginAS
from regrws.models.poc import PocLinkRef
from regrws.models.types import ZeroPaddedIPvAnyAddress, cidr_length_type

if TYPE_CHECKING:
    from regrws.models.error import Error
    from regrws.models.tickets import TicketRequest


class NetManager(BaseManager):
    """Custom Manager for Net Payloads"""

    def create(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError  # pragma: no cover

    def delete(
        self, instance: BaseModel, return_type: type[BaseModel] | None = None
    ) -> BaseModel | None:
        """This call will generate an automatically-processed ticketed request to delete the NET"""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        return super().delete(instance, TicketRequest)

    def remove(self, instance: Net) -> TicketRequest | Error | None:
        """This call will remove the network from the ARIN database. It is only applicable for reallocations or reassignments.
        It differs from the Delete NET call in that attachments can be sent using the NET payload."""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        url = instance.absolute_url
        if url:
            url = str(url) + "/remove"
            return self._do(  # type: ignore[return-value]
                "put",
                url,
                data=instance.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore[arg-type]
                return_type=TicketRequest,
            )
        return None  # pragma: no cover

    def reassign(self, instance: Net, net: Net) -> TicketRequest | Error | None:
        """This call performs a reassignment from the NET instance using the recipient information from the object."""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        url = instance.absolute_url
        if url:
            url = str(url) + "/reassign"
            return self._do(  # type: ignore[return-value]
                "put",
                url,
                data=net.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore[arg-type]
                return_type=TicketRequest,
            )
        return None  # pragma: no cover

    def reallocate(self, instance: Net, net: Net) -> TicketRequest | Error | None:
        """This call performs a reallocation from the NET instance using the recipient information from the object."""
        # Avoid circular import
        from regrws.models.tickets import TicketRequest

        url = instance.absolute_url
        if url:
            url = str(url) + "/reallocate"
            return self._do(  # type: ignore[return-value]
                "put",
                url,
                data=net.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore[arg-type]
                return_type=TicketRequest,
            )
        return None  # pragma: no cover

    def find_parent(
        self,
        start_address: ZeroPaddedIPvAnyAddress,
        end_address: ZeroPaddedIPvAnyAddress,
    ) -> Net | Error | None:
        """This call finds the parent of the network represented by the start and end IP range and returns a NET payload containing the details of the parent NET."""
        if self.model._endpoint:
            url = f"{self.api.base_url}{self.model._endpoint}/parentNet/{start_address}/{end_address}"
            return self._do("get", url)  # type: ignore[return-value]
        return None  # pragma: no cover

    def find_net(
        self,
        start_address: ZeroPaddedIPvAnyAddress,
        end_address: ZeroPaddedIPvAnyAddress,
    ) -> Net | Error | None:
        """This call finds the network details related to the start and end IP range.
        If multiple networks exist for the same IP range, then the most specific network is returned."""
        if self.model._endpoint:
            url = f"{self.api.base_url}{self.model._endpoint}/mostSpecificNet/{start_address}/{end_address}"
            return self._do("get", url)  # type: ignore[return-value]
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
    description: str | None = element(default=None)
    start_address: ZeroPaddedIPvAnyAddress = element(tag="startAddress")
    end_address: ZeroPaddedIPvAnyAddress | None = element(
        tag="endAddress", default=None
    )
    cidr_length: cidr_length_type | None = element(tag="cidrLength", default=None)

    @model_validator(mode="before")
    @classmethod
    def check_payload(cls, values: Any) -> Any:  # pragma: no cover
        results = values.get("end_address") is None, values.get("cidr_length") is None
        if all(results):
            raise ValueError("either `end_address` or `cidr_length` must be provided")
        return values


class Net(BaseModel, tag="net", nsmap=NSMAP, search_mode="unordered"):
    version: IPVersionEnum = element()
    comment: list[MultiLineElement] | None = wrapped(
        "comment", element(tag="line"), default=None
    )

    org_handle: str | None = element(tag="orgHandle", default=None)
    customer_handle: str | None = element(tag="customerHandle", default=None)

    handle: str | None = element(default=None)
    registration_date: str | None = element(tag="registrationDate", default=None)

    net_name: str | None = element(tag="netName", default=None)
    net_blocks: list[NetBlock] | None = wrapped(
        "netBlocks", element(tag="netBlock"), default=None
    )

    parent_net_handle: str | None = element(tag="parentNetHandle", default=None)

    origin_ases: list[OriginAS] | None = wrapped(
        "originASes", element(tag="originAS"), default=None
    )

    poc_links: list[PocLinkRef] | None = wrapped(
        "pocLinks", element(tag="pocLinkRef"), default=None
    )

    _endpoint: ClassVar[str] = "/net"
    _manager_class: ClassVar[type[BaseManager]] = NetManager

    @model_validator(mode="before")
    @classmethod
    def check_related_handle(cls, values: Any) -> Any:  # pragma: no cover
        results = values.get("org_handle"), values.get("customer_handle")
        results_are_none = (x is None for x in results)
        if all(results_are_none):
            raise ValueError(
                "either `org_handle` or `customer_handle` must be provided"
            )
        if all(results):
            raise ValueError(
                "`orgHandle` and `customerHandle` elements are mutually exclusive."
            )
        return values

    def remove(self) -> TicketRequest | Error | None:
        """Remove the Net from the ARIN database"""
        if self._manager is None:
            return None  # pragma: no cover
        return cast(NetManager, self._manager).remove(self)

    def reassign(self, net: Net) -> TicketRequest | Error | None:
        """Reassign the child Net to a different Org or Customer"""
        if self._manager is None:
            return None  # pragma: no cover
        return cast(NetManager, self._manager).reassign(self, net)

    def reallocate(self, net: Net) -> TicketRequest | Error | None:
        """Reallocate the child Net to a different Org or Customer"""
        if self._manager is None:
            return None  # pragma: no cover
        return cast(NetManager, self._manager).reallocate(self, net)
