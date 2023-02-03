"""Response hook for pydantic_xml and requests."""

from __future__ import annotations

from typing import Optional, Type, Dict

import requests
from pydantic_xml.model import BaseXmlModel


class Response(requests.Response):
    """An pydantic_xml-enabled :class:`requests.Response <requests.Response>` object."""

    def __init__(self, session: Session):
        super(Response, self).__init__()
        self._object: Type[BaseXmlModel] | None = None
        self.session = session

    @property
    def model(self) -> Type[BaseXmlModel] | BaseXmlModel | None:
        if not self._object:
            try:
                model: Type[BaseXmlModel] = self.session.handlers[self.status_code]
            except KeyError:
                raise RuntimeError(
                    f"Parser for status code {self.status_code} is missing in session."
                )
            self._object = model.from_xml(self.content)
        return self._object

    @classmethod
    def _from_response(cls, response, session: Session):
        pydantic_r = cls(session=session)
        pydantic_r.__dict__.update(response.__dict__)
        return pydantic_r


class Session(requests.Session):
    """A consumable session, for cookie persistence and connection pooling,
    amongst other things.
    """

    def __init__(self, handlers: Dict[int, Type[BaseXmlModel]], headers: Optional[dict] = None):
        super().__init__()
        self.handlers = handlers
        self.hooks["response"].append(self.response_hook)
        if headers:
            self.headers.update(headers)

    def response_hook(self, response, **kwargs) -> Response:
        """Replace reuqest's response by a regrws Response instance."""
        return Response._from_response(response, self)


class Endpoint:
    def __init__(self, session: Session) -> None:
        self.session = session