import pytest
import requests
import responses

from regrws.api.core import API
from regrws.models import POC, Customer, Error, Net, NetBlock, Org
from regrws.models.base import BaseModel

from .payloads import (CUSTOMER_PAYLOAD, ERROR_PAYLOAD, NET_PAYLOAD,
                       NETBLOCK_PAYLOAD, ORG_PAYLOAD, POC_PAYLOAD)

PARAMETERS = (
    (Org, ORG_PAYLOAD, "org"),
    (Customer, CUSTOMER_PAYLOAD, "customer"),
    # (NetBlock, NETBLOCK_PAYLOAD),
    # (Net, NET_PAYLOAD),
    # (Error, ERROR_PAYLOAD),
    # (POC, POC_PAYLOAD),
)


@pytest.mark.parametrize(
    (
        "model",
        "payload",
        "manager"
    ),
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
        api = API(api_key="APIKEY", base_url="https://reg.ote.arin.net/")
        assert api

        instance._api = api

        mocked_responses.get(
            f"{instance.absolute_url}?apikey=APIKEY",
            body=payload.encode(),
            status=200,
            content_type="application/xml",
        )
        resp = requests.get(f"{instance.absolute_url}?apikey=APIKEY")
        assert resp.status_code == 200

        api = API(api_key="APIKEY")
        manager = getattr(api, manager)
        inst = manager.get(instance.handle)
        assert inst