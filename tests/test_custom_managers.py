import pytest
import responses

from regrws.api import Api, constants
from regrws.models.customer import Customer

from .payloads import (
    CUSTOMER_PAYLOAD,
    NET_PAYLOAD,
    ORG_PAYLOAD,
    TICKET_PAYLOAD,
    TICKETED_REQUEST_PAYLOAD,
)


@pytest.fixture()
def api():
    return Api(api_key="APIKEY")


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_cust_manager(mocked_responses, api: type[Api]):
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1?apikey=APIKEY",
        body=NET_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.post(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1/customer?apikey=APIKEY",
        body=CUSTOMER_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    net = api.net.from_handle(handle="Net-10-0-0-0-1")
    customer = Customer.from_xml(CUSTOMER_PAYLOAD)
    assert customer is not None, "customer should not be None"
    api.customer.create_for_net(net=net, **customer.model_dump())


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
    params = instance.model_dump()
    params.pop("handle")
    assert api.org.create(**params)


def test_net_manager(mocked_responses, api: type[Api]):
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1?apikey=APIKEY",
        body=NET_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/net/parentNet/10.0.0.0/10.255.255.255?apikey=APIKEY",
        body=NET_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/net/mostSpecificNet/10.0.0.0/10.255.255.255?apikey=APIKEY",
        body=NET_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.delete(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1?apikey=APIKEY",
        body=TICKETED_REQUEST_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.put(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1/remove?apikey=APIKEY",
        body=TICKETED_REQUEST_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.put(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1/reassign?apikey=APIKEY",
        body=TICKETED_REQUEST_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )
    mocked_responses.put(
        "https://reg.ote.arin.net/rest/net/NET-10-0-0-0-1/reallocate?apikey=APIKEY",
        body=TICKETED_REQUEST_PAYLOAD.encode(),
        status=200,
        content_type=constants.CONTENT_TYPE,
    )

    with pytest.raises(NotImplementedError):
        api.net.create(**dict())

    instance = api.net.from_handle(handle="NET-10-0-0-0-1")
    assert instance is not None, "Instance should not be None"
    assert instance.delete()
    assert instance.remove()

    assert instance.reassign(instance)
    assert instance.reallocate(instance)

    assert api.net.find_parent("10.0.0.0", "10.255.255.255")
    assert api.net.find_net("10.0.0.0", "10.255.255.255")
