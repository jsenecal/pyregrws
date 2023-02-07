from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Literal, Optional

import requests

from regrws.arin_xml_encoder import ARINXmlEncoder
from regrws.models import Customer, Error, Org, Net, POC
from regrws.settings import Settings

from . import constants

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

    def __init__(self, handlers: Dict[int, XmlModelType], headers: Optional[dict] = None):
        super().__init__()
        self.handlers = handlers
        self.hooks["response"].append(self.response_hook)
        self.headers.update({"accept": constants.CONTENT_TYPE})
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
            kwargs = dict(base_url=constants.BASE_URL_DEFAULT)
            if base_url is not None:
                kwargs["base_url"] = base_url
            if api_key is not None:
                kwargs["api_key"] = api_key
            settings = Settings(**kwargs)  # type: ignore
        base_url = settings.base_url
        self.base_url = f"{base_url if base_url[-1] != '/' else base_url[:-1]}/rest"
        self.apikey = settings.api_key

        for model in [Customer, Net, Org, POC]:
            if hasattr(model, "_endpoint"):
                manager = Manager(api=self, model=model)
                endpoint = model._endpoint[1:]  # Remove leading "/"
                setattr(self, endpoint, manager)


class Manager:
    def __init__(self, api: API, model: type[BaseModel]) -> None:
        self.model = model
        self.api = api
        self.session = Session({200: model, 400: Error})
        self.url_params = {"apikey": self.api.apikey.get_secret_value()}

    @property
    def endpoint_url(self):
        if self.api and self.model._endpoint:
            return f"{self.api.base_url}{self.model._endpoint}"

    def _do(self, verb: Literal["get", "post", "put", "delete"], url: str, data: bytes | None = None):
        with self.session as s:
            session_method = getattr(s, verb)
            res: Response = session_method(url, params=self.url_params, data=data)  # type: ignore
            res.raise_for_unknown_status()

            if res.instance:
                res.instance._api = self.api
                res.instance._manager = self
            return res.instance

    def create(self, *args, **kwargs):
        instance = self.model(*args, **kwargs)
        instance._manager = self
        instance._api = self.api
        url = instance.absolute_url
        if url:
            return self._do(
                "post",
                url,
                instance.to_xml(encoder=ARINXmlEncoder(), encoding="UTF-8", skip_empty=True),
            )

    # retrieve
    def get(self, handle: str):
        if self.endpoint_url:
            handle = handle.upper()
            url = self.endpoint_url + f"/{handle}"
            return self._do("get", url)

    # update
    def save(self, instance: type[BaseModel]):
        url = instance.absolute_url
        if url:
            return self._do(
                "put", url, instance.to_xml(encoder=ARINXmlEncoder(), encoding="UTF-8", skip_empty=True)
            )

    # delete
    def delete(self, instance: type[BaseModel]):
        url = instance.absolute_url
        if url:
            return self._do("delete", url)
