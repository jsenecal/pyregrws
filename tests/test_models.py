import pytest

from regrws.models import Customer, NetBlock, Org, Net
from regrws.arin_xml_encoder import ARINXmlEncoder
from .payloads import CUSTOMER_PAYLOAD, NETBLOCK_PAYLOAD, ORG_PAYLOAD, NET_PAYLOAD


PARAMETERS = [(Org, ORG_PAYLOAD), (Customer, CUSTOMER_PAYLOAD), (NetBlock, NETBLOCK_PAYLOAD), (Net, NET_PAYLOAD)]


@pytest.mark.parametrize(
    (
        "model",
        "payload",
    ),
    PARAMETERS,
)
class TestModels:
    @pytest.fixture
    def instance(self, model, payload):
        return model.from_xml(payload)

    def test_from_xml(self, instance):
        assert instance is not None

    def test_to_xml(self, instance):
        instance_xml = instance.to_xml(encoder=ARINXmlEncoder(), pretty_print=True, encoding="UTF-8", skip_empty=True).decode()
        print("\n" + instance_xml)
        assert instance_xml is not False
