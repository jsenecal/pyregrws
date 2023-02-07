from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from regrws.arin_xml_encoder import ARINXmlEncoder

if TYPE_CHECKING:
    from regrws.models.base import BaseModel
    from regrws.api.core import Api

class BaseManager:
    def __init__(self, api: Api, model: type[BaseModel]) -> None:
        # prevent circular import
        from regrws.models import Error
        from regrws.api.core import Session


        self.model = model
        self.api = api
        self.session = Session({200: model, 400: Error})
        self.url_params = {"apikey": self.api.apikey.get_secret_value()}

    @property
    def endpoint_url(self):
        if self.api and self.model._endpoint:
            return f"{self.api.base_url}{self.model._endpoint}"

    def _do(
        self, verb: Literal["get", "post", "put", "delete"], url: str, data: bytes | None = None
    ):
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
                "put",
                url,
                instance.to_xml(encoder=ARINXmlEncoder(), encoding="UTF-8", skip_empty=True),
            )

    # delete
    def delete(self, instance: type[BaseModel]):
        url = instance.absolute_url
        if url:
            return self._do("delete", url)
