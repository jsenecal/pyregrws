from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

import requests

from regrws.settings import Settings

from regrws.api import constants

if TYPE_CHECKING:
    from regrws.models.types import xmlmodel_type


class Response(requests.Response):
    """A pydantic_xml-enabled :class:`requests.Response <requests.Response>` object.

    This class extends the standard requests.Response to automatically parse
    XML content into pydantic models based on HTTP status codes.
    """

    def __init__(self, session: Session):
        super(Response, self).__init__()
        self._object: xmlmodel_type | None = None
        self.session = session

    @property
    def instance(self) -> xmlmodel_type | None:
        """Get pydantic_xml instance from request content.

        Returns:
            The parsed pydantic model instance or None if parsing fails.

        Raises:
            RuntimeError: If no parser is registered for the response status code.
        """
        if not self._object:
            try:
                model: xmlmodel_type = self.session.handlers[self.status_code]
            except KeyError:
                raise RuntimeError(
                    f"Parser for status code {self.status_code} is missing in session."
                )
            self._object = model.from_xml(self.content)
        return self._object

    def raise_for_unknown_status(self):
        """Raises :class:`HTTPError` for unknown status codes.

        Only raises an HTTPError if the status code is not registered
        in the session's handlers dictionary.
        """

        if self.status_code not in self.session.handlers.keys():
            super().raise_for_status()

    @classmethod
    def _from_response(cls, response, session: Session):
        pydantic_r = cls(session=session)
        pydantic_r.__dict__.update(response.__dict__)
        return pydantic_r


class Session(requests.Session):
    """A consumable session with automatic XML parsing capabilities.

    This session automatically converts responses to Response objects that can
    parse XML content into pydantic models based on HTTP status codes.

    Args:
        handlers: Dictionary mapping HTTP status codes to pydantic model classes.
        headers: Optional additional headers to include in requests.
    """

    def __init__(
        self, handlers: Dict[int, xmlmodel_type], headers: Optional[dict] = None
    ):
        super().__init__()
        self.handlers = handlers
        self.hooks["response"].append(self.response_hook)
        self.headers.update({"accept": constants.CONTENT_TYPE})
        if headers:
            self.headers.update(headers)  # pragma: no cover

    def response_hook(self, response, **kwargs) -> Response:
        """Replace request's Response with a regrws Response instance.

        This hook is automatically called for all responses and converts
        the standard requests.Response to our custom Response class.

        Args:
            response: The original requests.Response object.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            A regrws Response instance with XML parsing capabilities.
        """
        return Response._from_response(response, self)


class Api:
    """The main API client for interacting with ARIN's Reg-RWS service.

    This class serves as the primary entry point for the regrws library.
    It automatically creates manager instances for each supported model type
    and provides a unified interface for CRUD operations.

    Args:
        base_url: Base URL for the ARIN Reg-RWS API. Defaults to ARIN production.
        api_key: Your ARIN API key. Can also be set via REGRWS_API_KEY env var.
        settings: Optional Settings object for advanced configuration.

    Attributes:
        poc: Manager for POC (Point of Contact) operations.
        org: Manager for Organization operations.
        net: Manager for Network operations.
        customer: Manager for Customer operations.

    Example:
        >>> api = Api(api_key="your-api-key")
        >>> poc = api.poc.from_handle("EXAMPLE-ARIN")
        >>> print(f"POC: {poc.first_name} {poc.last_name}")
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        settings: Settings | None = None,
    ):
        # avoid circular imports
        from regrws.models import (  # pylint: disable=import-outside-toplevel
            Customer,
            Net,
            Org,
            Poc,
        )

        if settings is None:
            kwargs = dict(base_url=constants.BASE_URL_DEFAULT)
            if base_url is not None:
                kwargs["base_url"] = base_url
            if api_key is not None:
                kwargs["api_key"] = api_key
            settings = Settings(**kwargs)  # type: ignore
        base_url = settings.base_url
        self.base_url = f"{base_url if base_url[-1] != '/' else base_url[:-1]}/rest"
        self.apikey = settings.api_key

        for model in [Customer, Net, Org, Poc]:
            if hasattr(model, "_endpoint"):
                manager = model._manager_class(api=self, model=model)
                endpoint = model._endpoint[1:]  # Remove leading "/"
                setattr(self, endpoint, manager)
