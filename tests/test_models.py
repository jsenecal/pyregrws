import pytest

from regrws.models import Customer, NetBlock, Org
from regrws.xml_encoder import IPaddressXmlEncoder

from .payloads import CUSTOMER_PAYLOAD, NETBLOCK_PAYLOAD, ORG_PAYLOAD


PARAMETERS = [
    (Org, ORG_PAYLOAD),
    (Customer, CUSTOMER_PAYLOAD),
    (NetBlock, NETBLOCK_PAYLOAD),
]


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
        org_xml = org.to_xml(
            encoder=IPaddressXmlEncoder(), pretty_print=True, encoding="UTF-8"
        ).decode()
        print("\n"+org_xml)
        assert org_xml is not False
