import pytest
import responses
import requests
from pydantic.error_wrappers import ValidationError

from regrws.api.core import Response, Session


from regrws.models import Org
from .payloads import ORG_PAYLOAD


def test_valid_parser_and_model(cov):
    """Ensure parsing and model logic work."""
    res = Response(Session({200: Org}))
    res.status_code = 200
    res._content = ORG_PAYLOAD.encode()
    assert res.model


def test_invalid_model(cov):
    """Ensure that proper exception bubbles up."""
    res = Response(Session({200: Org}))
    res.status_code = 200
    res._content = b'<org xmlns="http://www.arin.net/regrws/core/v1" ></org>'
    with pytest.raises(ValidationError) as exc:
        res.model
    exc.match("type=value_error.missing")


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_requests_wrapper(mocked_responses):
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/org/ARIN?apikey=APIKEY",
        body=ORG_PAYLOAD.encode(),
        status=200,
        content_type="application/xml",
    )
    resp = requests.get("https://reg.ote.arin.net/rest/org/ARIN?apikey=APIKEY")
    assert resp.status_code == 200
    with Session(
        {200: Org}, headers={"accept": "application/xml"}
    ) as session:
        org_id = "ARIN"
        res = session.get(
            f"https://reg.ote.arin.net/rest/org/{org_id}",  params={"apikey": "APIKEY"}
        )
        res.raise_for_status()
        org: Org = res.model
        assert org is not None