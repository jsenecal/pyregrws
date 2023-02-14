from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from regrws.api.core import Response
from regrws.arin_xml_encoder import ARINXmlEncoder

if TYPE_CHECKING:
    from regrws.api.core import Api
    from regrws.models.base import BaseModel


class BaseManager:
    def __init__(self, api: Api, model: type[BaseModel]) -> None:
        # prevent circular import
        from regrws.api.core import Session
        from regrws.models import Error

        self.model = model
        self.api = api
        self.session = Session({200: model, 400: Error})
        self.url_params = {"apikey": self.api.apikey.get_secret_value()}

    @property
    def endpoint_url(self):
        if self.api and self.model._endpoint:
            return f"{self.api.base_url}{self.model._endpoint}"

    def _do(
        self,
        verb: Literal["get", "post", "put", "delete"],
        url: str,
        data: bytes | None = None,
    ):
        with self.session as session:
            session_method = getattr(session, verb)
            res: Response = session_method(
                url, params=self.url_params, data=data
            )  # type: ignore
            res.raise_for_unknown_status()

            if res.instance:
                res.instance.manager = self  # type: ignore
            return res.instance

    def create(self, *args, **kwargs):
        instance = self.model(*args, **kwargs)
        instance.manager = self
        url = instance.absolute_url
        if url:
            return self._do(
                "post",
                url,
                instance.to_xml(
                    encoder=ARINXmlEncoder(), encoding="UTF-8", skip_empty=True
                ),  # type: ignore
            )

    # retrieve
    def from_handle(self, handle: str):
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
                instance.to_xml(
                    encoder=ARINXmlEncoder(), encoding="UTF-8", skip_empty=True
                ),  # type: ignore
            )

    # delete
    def delete(self, instance: type[BaseModel]):
        url = instance.absolute_url
        if url:
            return self._do("delete", url)
