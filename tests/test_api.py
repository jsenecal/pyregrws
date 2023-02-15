import pytest
import responses

from regrws.api import constants
from regrws.api.core import Api
from regrws.models import Poc, Net, Org
from regrws.models.base import BaseModel

from .payloads import (
    NET_PAYLOAD,
    ORG_PAYLOAD,
    POC_PAYLOAD,
)

SKIP_MSG = "no way to properly test this method against this endpoint"

PARAMETERS = (
    (Net, NET_PAYLOAD, "net", ["create", "delete"]),
    (Org, ORG_PAYLOAD, "org", ["create"]),
    (Poc, POC_PAYLOAD, "poc", []),
)


@pytest.mark.parametrize(
    ("model", "payload", "manager", "skip"),
    PARAMETERS,
)
class TestAPI:
    @pytest.fixture
    def mocked_responses(self):
        with responses.RequestsMock() as rsps:
            yield rsps

    @pytest.fixture
    def instance(self, model, payload, cov):
        return model.from_xml(payload)

    @pytest.fixture
    def api(self):
        return Api(api_key="APIKEY", base_url=constants.BASE_URL_DEFAULT)

    def test_manager_from_handle(
        self, mocked_responses, instance: BaseModel, api, payload, manager, skip, cov
    ):
        if "get" in skip:
            pytest.skip(SKIP_MSG) # pragma: no cover

        instance.manager = getattr(api, manager)

        mocked_responses.get(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        inst = instance.manager.from_handle(instance.handle)
        assert inst

    def test_manager_put(
        self, mocked_responses, instance: BaseModel, api, payload, manager, skip, cov
    ):
        if "put" in skip:
            pytest.skip(SKIP_MSG) # pragma: no cover

        instance.manager = getattr(api, manager)

        mocked_responses.put(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        instance.save()
        assert instance

    def test_manager_delete(
        self, mocked_responses, instance: BaseModel, api, payload, manager, skip, cov
    ):
        if "delete" in skip:
            pytest.skip(SKIP_MSG)

        instance.manager = getattr(api, manager)

        mocked_responses.delete(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        instance.delete()
        assert instance

    def test_manager_create(
        self, mocked_responses, instance: BaseModel, api, payload, manager, skip, cov
    ):
        if "create" in skip:
            pytest.skip(SKIP_MSG)

        manager = getattr(api, manager)
        instance.manager = manager
        mocked_responses.post(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        new_insance = manager.create(**instance.dict())
        assert new_insance
