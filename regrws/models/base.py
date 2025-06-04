from __future__ import annotations

import inspect
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, no_type_check

from pydantic_xml.model import BaseXmlModel

from regrws.api.manager import BaseManager

if TYPE_CHECKING:
    from regrws.api.core import Api


NSMAP = {"": "http://www.arin.net/regrws/core/v1"}


class BaseModel(BaseXmlModel):
    """Base model class for all ARIN Reg-RWS resources.

    This class extends pydantic-xml's BaseXmlModel with ARIN-specific
    functionality including automatic manager integration and XML namespace
    configuration.

    Attributes:
        _endpoint: The API endpoint path for this resource type.
        _handle: The attribute name used as the resource handle (default: 'handle').
        _manager_class: The manager class to use for API operations.
    """

    _endpoint: ClassVar[str]
    _handle: ClassVar[str] = "handle"
    _manager_class: ClassVar[type[BaseManager]] = BaseManager

    _api: Api
    _manager: BaseManager

    class Config:
        anystr_strip_whitespace = True
        underscore_attrs_are_private = True

        xml_encoders = {
            type(bool): lambda v: "true" if v else "false",
            type(Enum): lambda v: str(v.value),
        }

    @property
    def absolute_url(self) -> str | None:
        """Get the absolute URL for this resource.

        Returns:
            The full API URL for this resource, or None if no API or endpoint is set.
        """
        if self._api and self._endpoint:
            handle = getattr(self, self._handle)
            if handle:
                return f"{self._api.base_url}{self._endpoint}/{handle}"
            return f"{self._api.base_url}{self._endpoint}/"
        return None  # pragma: no cover

    def save(self):
        """Save changes to this resource.

        Returns:
            The updated resource instance from the API response.
        """
        return self._manager.save(self)

    def delete(self):
        """Delete this resource.

        Returns:
            The response from the delete operation.
        """
        return self._manager.delete(self)

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager: BaseManager):
        """Set the API Manager to the model instance.

        Args:
            manager: The BaseManager instance to associate with this model.
        """
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
