from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pydantic_xml.model import BaseXmlModel

if TYPE_CHECKING:
    from regrws.api.core import API, Manager



NSMAP = {"": "http://www.arin.net/regrws/core/v1"}


class BaseModel(BaseXmlModel):

    _endpoint: ClassVar[str]
    _handle: ClassVar[str] = "handle"

    _api: API
    _manager: Manager

    class Config:
        anystr_strip_whitespace = True
        underscore_attrs_are_private = True

    @property
    def absolute_url(self):
        if self._api and self._endpoint:
            return f"{self._api.base_url}{self._endpoint}/{getattr(self, self._handle)}"

    