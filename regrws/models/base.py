from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, ClassVar, no_type_check

from pydantic_xml.model import BaseXmlModel

from regrws.api.manager import BaseManager

if TYPE_CHECKING:
    from regrws.api.core import Api


NSMAP = {"": "http://www.arin.net/regrws/core/v1"}


class BaseModel(BaseXmlModel):
    _endpoint: ClassVar[str]
    _handle: ClassVar[str] = "handle"
    _manager_class: ClassVar[type[BaseManager]] = BaseManager

    _api: Api
    _manager: BaseManager

    class Config:
        anystr_strip_whitespace = True
        underscore_attrs_are_private = True

    @property
    def absolute_url(self) -> str | None:
        if self._api and self._endpoint:
            handle = getattr(self, self._handle)
            if handle:
                return f"{self._api.base_url}{self._endpoint}/{handle}"
            return f"{self._api.base_url}{self._endpoint}/"
        return None  # pragma: no cover

    def save(self):
        return self._manager.save(self)

    def delete(self):
        return self._manager.delete(self)

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager: BaseManager):
        """Set the API Manager to the model instance"""
        self._manager = manager
        self._api = manager.api

    @no_type_check
    def __setattr__(self, name, value):
        """
        Allows proper use of properties with setters
        See https://github.com/pydantic/pydantic/issues/1577
        """
        try:
            super().__setattr__(name, value)
        except ValueError as exc:
            setters = inspect.getmembers(
                self.__class__,
                predicate=lambda x: isinstance(x, property) and x.fset is not None,
            )
            for setter_name, _ in setters:
                if setter_name == name:
                    object.__setattr__(self, name, value)
                    break
            else:
                raise exc  # pragma: no cover
