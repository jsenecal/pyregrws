import pytest
import responses
import requests
from pydantic.error_wrappers import ValidationError

from regrws.api.core import Response, Session


from regrws.models import Org, Error
from .payloads import ORG_PAYLOAD, ERROR_PAYLOAD


def test_valid_parser_and_model(cov):
    """Ensure parsing and model logic work."""
    res = Response(Session({200: Org}))
    res.status_code = 200
    res._content = ORG_PAYLOAD.encode()
    assert res.instance


def test_invalid_model(cov):
    """Ensure that proper exception bubbles up."""
    res = Response(Session({200: Org}))
    res.status_code = 200
    res._content = b'<org xmlns="http://www.arin.net/regrws/core/v1" ></org>'
    with pytest.raises(ValidationError) as exc:
        res.instance
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

    with Session({200: Org}) as session:
        org_id = "ARIN"
        res: Response = session.get(
            f"https://reg.ote.arin.net/rest/org/{org_id}", params={"apikey": "APIKEY"}
        )
        assert res.status_code == 200
        res.raise_for_status()
        org: Org = res.instance
        assert org
        assert isinstance(org, Org)

def test_requests_wrapper_with_errors(mocked_responses):
    mocked_responses.get(
        "https://reg.ote.arin.net/rest/org/ARIN?apikey=APIKEY",
        body=ERROR_PAYLOAD.encode(),
        status=400,
        content_type="application/xml",
    )
    resp = requests.get("https://reg.ote.arin.net/rest/org/ARIN?apikey=APIKEY")
    assert resp.status_code == 400

    with Session({400: Error}) as session:
        org_id = "ARIN"
        res: Response = session.get(
            f"https://reg.ote.arin.net/rest/org/{org_id}", params={"apikey": "APIKEY"}
        )
        assert res.status_code == 400
        with pytest.raises(requests.HTTPError):
            res.raise_for_status()
        res.raise_for_unknown_status()
        err: Error = res.instance
        assert Error
        assert isinstance(err, Error)

    with Session({200: Org}) as session:
        org_id = "ARIN"
        res: Response = session.get(
            f"https://reg.ote.arin.net/rest/org/{org_id}", params={"apikey": "APIKEY"}
        )
        assert res.status_code == 400
        with pytest.raises(RuntimeError, match=f"Parser for status code {res.status_code} is missing in session."):
            res.instance