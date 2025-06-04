from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from regrws.api.core import Response


if TYPE_CHECKING:
    from regrws.api.core import Api
    from regrws.models.base import BaseModel


class BaseManager:
    """Base manager class providing CRUD operations for ARIN resources.

    This class provides a standard interface for Create, Read, Update, and Delete
    operations on ARIN resources through the Reg-RWS API.

    Args:
        api: The Api instance to use for HTTP requests.
        model: The pydantic model class this manager operates on.
    """

    def __init__(self, api: Api, model: type[BaseModel]) -> None:
        self.model = model
        self.api = api
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
        return_type: type[BaseModel] | None = None,
    ):
        # prevent circular import
        from regrws.api.core import Session
        from regrws.models import Error

        handlers = {200: return_type or self.model}
        handlers.update({i: Error for i in [400, 401, 403, 404, 405, 406, 409]})
        with Session(handlers) as session:  # type: ignore
            session_method = getattr(session, verb)
            res: Response = session_method(url, params=self.url_params, data=data)  # type: ignore
            res.raise_for_unknown_status()

            if res.instance:
                related_model = res.instance.__class__
                res.instance.manager = related_model._manager_class(
                    api=self.api, model=related_model
                )  # type: ignore
            return res.instance

    def create(self, return_type: type[BaseModel] | None = None, *args, **kwargs):
        """Create a new resource.

        Args:
            return_type: Optional model class to parse the response into.
            *args: Positional arguments to pass to the model constructor.
            **kwargs: Keyword arguments to pass to the model constructor.

        Returns:
            The created resource instance or None if creation failed.
        """
        instance = self.model(*args, **kwargs)
        instance.manager = self
        url = instance.absolute_url
        if url:
            return self._do(
                "post",
                url,
                instance.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore
                return_type,
            )

    # retrieve
    def from_handle(self, handle: str):
        """Retrieve a resource by its handle.

        Args:
            handle: The ARIN handle of the resource to retrieve.

        Returns:
            The retrieved resource instance or None if not found.
        """
        if self.endpoint_url:
            handle = handle.upper()
            url = self.endpoint_url + f"/{handle}"
            return self._do("get", url)

    # update
    def save(self, instance: BaseModel):
        """Update an existing resource.

        Args:
            instance: The model instance to save. Must have a valid handle.

        Returns:
            The updated resource instance or None if update failed.
        """
        url = instance.absolute_url
        if url:
            return self._do(
                "put",
                url,
                instance.to_xml(encoding="UTF-8", skip_empty=True),  # type: ignore
            )

    # delete
    def delete(
        self,
        instance: type[BaseModel],
        return_type: type[BaseModel] | None = None,
    ):
        """Delete a resource.

        Args:
            instance: The model instance to delete. Must have a valid handle.
            return_type: Optional model class to parse the response into.

        Returns:
            The response from the delete operation or None if deletion failed.
        """
        url = str(instance.absolute_url)
        if url:
            return self._do("delete", url, return_type=return_type)
