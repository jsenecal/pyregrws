from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

import requests

from regrws.models import Customer, Error, Org
from regrws.settings import Settings

from .constants import BASE_URL_DEFAULT

if TYPE_CHECKING:
    from regrws.models.base import BaseModel
    from regrws.models.types import XmlModelType


class Response(requests.Response):
    """An pydantic_xml-enabled :class:`requests.Response <requests.Response>` object."""

    def __init__(self, session: Session):
        super(Response, self).__init__()
        self._object: XmlModelType | None = None
        self.session = session

    @property
    def instance(self) -> XmlModelType | None:
        if not self._object:
            try:
                model: XmlModelType = self.session.handlers[self.status_code]
            except KeyError:
                raise RuntimeError(
                    f"Parser for status code {self.status_code} is missing in session."
                )
            self._object = model.from_xml(self.content)
        return self._object

    def raise_for_unknown_status(self):
        """Raises :class:`HTTPError`, if one occurred."""

        if not self.status_code in self.session.handlers.keys():
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

    def __init__(self, handlers: Dict[int, XmlModelType], headers: Optional[dict] = None):
        super().__init__()
        self.handlers = handlers
        self.hooks["response"].append(self.response_hook)
        self.headers.update({"accept": "application/xml"})
        if headers:
            self.headers.update(headers)

    def response_hook(self, response, **kwargs) -> Response:
        """Replace request's Response by a regrws Response instance."""
        return Response._from_response(response, self)


class API:
    """The API object is the point of entry to regrws."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        settings: Settings | None = None,
    ):
        if settings is None:
            kwargs = dict(base_url=BASE_URL_DEFAULT)
            if base_url is not None:
                kwargs["base_url"] = base_url
            if api_key is not None:
                kwargs["api_key"] = api_key
            settings = Settings(**kwargs)  # type: ignore
        base_url = settings.base_url
        self.base_url = f"{base_url if base_url[-1] != '/' else base_url[:-1]}/rest"
        self.apikey = settings.api_key

        self.org = Manager(api=self, model=Org)
        self.customer = Manager(api=self, model=Customer)


class Manager:
    def __init__(self, api: API, model: type[BaseModel]) -> None:
        self.model = model
        self.api = api
        self.session = Session({200: model, 400: Error})

    @property
    def endpoint_url(self):
        if self.api and self.model._endpoint:
            return f"{self.api.base_url}{self.model._endpoint}"

    @property
    def absolute_url(self):
        try:
            return f"{self.endpoint_url}/{getattr(self.model, self.model._handle)}"
        except AttributeError:
            pass

    # create
    def create(self, *args, **kwargs):
        raise NotImplementedError

    # retrieve
    def get(self, handle: str):
        handle = handle.upper()
        with self.session as s:
            res: Response = s.get(self.endpoint_url + f"/{handle}", params={"apikey": self.api.apikey.get_secret_value()})  # type: ignore
            res.raise_for_unknown_status()

            if res.instance:
                res.instance._api = self.api
                res.instance._manager = self
            return res.instance

    # update
    def save(self, *args, **kwargs):
        raise NotImplementedError

    # delete
    def delete(self, *args, **kwargs):
        raise NotImplementedError