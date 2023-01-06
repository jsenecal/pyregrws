import pytest

from regrws.models import Org, Customer

from .payloads import ORG_PAYLOAD, CUSTOMER_PAYLOAD

PARAMETERS = [(Org, ORG_PAYLOAD), (Customer, CUSTOMER_PAYLOAD)]


@pytest.mark.parametrize(
    (
        "model",
        "payload",
    ),
    PARAMETERS,
)
class TestModels:
    @pytest.fixture
    def org(self, model, payload):
        return model.from_xml(payload)

    def test_from_xml(self, org):
        assert org is not None

    def test_to_xml(self, org):
        org_xml = org.to_xml(pretty_print=True, encoding="UTF-8")
        assert org_xml is not False
