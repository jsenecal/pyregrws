"""Ticket and related models"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic_xml.model import element, wrapped

from regrws.models.base import NSMAP, BaseModel
from regrws.models.nested import Attachment, MultiLineElement
from regrws.models.net import Net

TICKET_NSMAP = NSMAP
TICKET_NSMAP.update(
    {
        "mv1": "http://www.arin.net/regrws/messages/v1",
        "stv1": "http://www.arin.net/regrws/shared-ticket/v1",
    }
)


class TicketMessage(
    BaseModel,
    tag="message",
    nsmap=TICKET_NSMAP,
    search_mode="unordered"
):
    message_id: str = element(tag="messageId", ns="mv1")
    created_date: str = element(tag="createdDate", ns="mv1")
    subject: str = element()
    text: List[MultiLineElement] = wrapped("text", element(tag="line"))
    category: str = element()
    attachments: List[Attachment] = wrapped("attachments", element(tag="attachment"))


class Ticket(BaseModel, tag="ticket", nsmap=NSMAP, search_mode="unordered"):
    messages: List[TicketMessage] = wrapped("messages", element(tag="message"))
    ticket_no: str = element(tag="ticketNo")
    shared: bool | None = element(ns="stv1")
    org_handle: str | None = element(tag="orgHandle", ns="stv1")
    created_date: str = element(tag="createdDate")
    resolved_date: str = element(tag="resolvedDate")
    closed_date: str = element(tag="closedDate")
    updated_date: str = element(tag="updatedDate")
    web_ticket_type: Literal[
        "POC_RECOVERY",
        "QUESTION",
        "ASSOCIATIONS_REPORT",
        "REASSIGNMENT_REPORT",
        "ORG_CREATE",
        "EDIT_ORG_NAME",
        "ORG_RECOVERY",
        "TRANSFER_LISTING_SERVICE",
        "IPV4_SIMPLE_REASSIGN",
        "IPV4_DETAILED_REASSIGN",
        "IPV4_REALLOCATE",
        "IPV6_DETAILED_REASSIGN",
        "IPV6_REALLOCATE",
        "NET_DELETE_REQUEST",
        "ISP_IPV4_REQUEST",
        "ISP_IPV6_REQUEST",
        "CREATE_RESOURCE_CERTIFICATE",
        "CREATE_ROA",
        "END_USER_IPV4_REQUEST",
        "END_USER_IPV6_REQUEST",
        "ASN_REQUEST",
        "EDIT_BILLING_CONTACT_INFO",
        "ANY",
    ] = element(tag="webTicketType")

    web_ticket_status: Literal[
        "PENDING_CONFIRMATION",
        "PENDING_REVIEW",
        "ASSIGNED",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED",
        "APPROVED",
        "ANY",
        "ANY_OPEN",
    ] = element(tag="webTicketStatus")

    web_ticket_resolution: Literal[
        "ACCEPTED",
        "DENIED",
        "ABANDONED",
        "ANSWERED",
        "PROCESSED",
        "DUPLICATE",
        "WITHDRAWN",
        "UNSUCCESSFUL",
        "OTHER",
    ] = element(tag="webTicketResolution")


class TicketRequest(
    BaseModel, tag="ticketedRequest", nsmap=NSMAP, search_mode="unordered"
):
    ticket: Optional[Ticket] = element(tag="ticket")
    net: Optional[Net] = element(tag="net")
