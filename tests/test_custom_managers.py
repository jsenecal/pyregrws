import pytest
import responses

from regrws.api import Api, constants

from .payloads import (
    ORG_PAYLOAD,
    TICKET_PAYLOAD
)


@pytest.fixture()
def api():
    return Api(api_key="APIKEY")


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

def test_org_manager(mocked_responses, api: type[Api]):
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/org/ARIN?apikey=APIKEY",
        body=ORG_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.post(
        "https://reg.ote.arin.net/rest/org/?apikey=APIKEY",
        body=TICKET_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    instance = api.org.from_handle(handle="ARIN")
    assert instance is not None, "Instance should not be None"
    params = instance.dict()
    params.pop("handle")
    instance = api.org.create(**params)
    assert instance is not None, "Failed to create instance"
