from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

import requests

from regrws.settings import Settings

from . import constants

if TYPE_CHECKING:
    from regrws.models.types import xmlmodel_type


class Response(requests.Response):
    """An pydantic_xml-enabled :class:`requests.Response <requests.Response>` object."""

    def __init__(self, session: Session):
        super(Response, self).__init__()
        self._object: xmlmodel_type | None = None
        self.session = session

    @property
    def instance(self) -> xmlmodel_type | None:
        """Get pydantic_xml instance from request content"""
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
        """Raises :class:`HTTPError`, if one occurred."""

        if self.status_code not in self.session.handlers.keys():
            super().raise_for_status()

    @classmethod
    def _from_response(cls, response, session: Session):
        pydantic_r = cls(session=session)
        pydantic_r.__dict__.update(response.__dict__)
        return pydantic_r


class Session(requests.Session):
    """A consumable session, for cookie persistence and connection pooling,
    amongst other things.
    """

    def __init__(
        self, handlers: Dict[int, xmlmodel_type], headers: Optional[dict] = None
    ):
        super().__init__()
        self.handlers = handlers
        self.hooks["response"].append(self.response_hook)
        self.headers.update({"accept": constants.CONTENT_TYPE})
        if headers:
            self.headers.update(headers)

    def response_hook(self, response, **kwargs) -> Response:
        """Replace request's Response by a regrws Response instance."""
        return Response._from_response(response, self)


class Api:
    """The Api object is the point of entry to regrws."""

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
