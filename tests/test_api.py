import pytest
import responses

from regrws.api import constants
from regrws.api.core import API
from regrws.models import POC, Customer, Net, Org
from regrws.models.base import BaseModel

from .payloads import (
    CUSTOMER_PAYLOAD,
    ERROR_PAYLOAD,
    NET_PAYLOAD,
    NETBLOCK_PAYLOAD,
    ORG_PAYLOAD,
    POC_PAYLOAD,
)

PARAMETERS = (
    (Customer, CUSTOMER_PAYLOAD, "customer"),
    (Net, NET_PAYLOAD, "net"),
    (Org, ORG_PAYLOAD, "org"),
    (POC, POC_PAYLOAD, "poc"),
)


@pytest.mark.parametrize(
    ("model", "payload", "manager"),
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

    def test_manager_get(self, mocked_responses, instance: BaseModel, payload, manager, cov):
        api = API(api_key="APIKEY", base_url=constants.BASE_URL_DEFAULT)
        assert api

        instance._api = api

        mocked_responses.get(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        manager = getattr(api, manager)
        inst = manager.get(instance.handle)
        assert inst

    def test_manager_put(self, mocked_responses, instance: BaseModel, payload, manager, cov):
        api = API(api_key="APIKEY", base_url=constants.BASE_URL_DEFAULT)
        assert api

        instance._api = api
        instance._manager = getattr(api, manager)

        mocked_responses.put(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        instance.save()
        assert instance

    def test_manager_delete(self, mocked_responses, instance: BaseModel, payload, manager, cov):
        api = API(api_key="APIKEY", base_url=constants.BASE_URL_DEFAULT)
        assert api

        instance._api = api
        instance._manager = getattr(api, manager)

        mocked_responses.delete(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        instance.delete()
        assert instance

    def test_manager_create(self, mocked_responses, instance: BaseModel, payload, manager, cov):
        api = API(api_key="APIKEY", base_url=constants.BASE_URL_DEFAULT)
        assert api
        instance._api = api

        manager = getattr(api, manager)

        mocked_responses.post(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type=constants.CONTENT_TYPE,
        )

        new_insance = manager.create(**instance.dict())
        assert new_insance
