from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pydantic import ConfigDict, PrivateAttr
from pydantic_xml import BaseXmlModel

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

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    _endpoint: ClassVar[str]
    _handle: ClassVar[str] = "handle"
    _manager_class: ClassVar[type[BaseManager]] = BaseManager

    _api: Api = PrivateAttr()
    _manager: BaseManager = PrivateAttr()

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
