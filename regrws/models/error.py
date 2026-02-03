"""Error Model"""

from typing import List, Literal, Optional

from pydantic_xml.model import element, wrapped

from regrws.models.base import NSMAP, BaseModel


class ErrorComponent(BaseModel, tag="component", nsmap=NSMAP, search_mode="unordered"):
    """
    Component of the Error payload
    https://www.arin.net/resources/manage/regrws/payloads/#error-payload
    """

    name: str = element()
    message: str = element()


class Error(BaseModel, tag="error", nsmap=NSMAP, search_mode="unordered"):
    """https://www.arin.net/resources/manage/regrws/payloads/#error-payload"""

    message: str = element()
    code: Literal[
        "E_SCHEMA_VALIDATION",
        "E_ENTITY_VALIDATION",
        "E_OBJECT_NOT_FOUND",
        "E_AUTHENTICATION",
        "E_NOT_REMOVEABLE",
        "E_BAD_REQUEST",
        "E_OUTAGE",
        "E_UNSPECIFIED",
    ] = element()
    components: Optional[List[ErrorComponent]] = wrapped("components", element(tag="component"))
    additionnal_info: List[str] = wrapped(
        "additionalInfo", element(tag="message", default_factory=list)
    )
