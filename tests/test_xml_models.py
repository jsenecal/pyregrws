import pytest


from regrws.models import Customer, Error, Org, Poc
from regrws.models.net import Net, NetBlock
from regrws.models.tickets import TicketRequest

from .payloads import (
    CUSTOMER_PAYLOAD,
    ERROR_PAYLOAD,
    NET_PAYLOAD,
    NETBLOCK_PAYLOAD,
    ORG_PAYLOAD,
    POC_PAYLOAD,
    TICKETED_REQUEST_PAYLOAD,
)

PARAMETERS = (
    (Org, ORG_PAYLOAD),
    (Customer, CUSTOMER_PAYLOAD),
    (NetBlock, NETBLOCK_PAYLOAD),
    (Net, NET_PAYLOAD),
    (Error, ERROR_PAYLOAD),
    (Poc, POC_PAYLOAD),
    (TicketRequest, TICKETED_REQUEST_PAYLOAD),
)


@pytest.mark.parametrize(
    (
        "model",
        "payload",
    ),
    PARAMETERS,
)
class TestModels:
    @pytest.fixture
    def instance(self, model, payload, cov):
        return model.from_xml(payload)

    def test_from_xml(self, instance, cov):
        assert instance is not None

    def test_to_xml(self, instance, cov):
        instance_xml = instance.to_xml(
            pretty_print=True,
            encoding="UTF-8",
            skip_empty=True,
        ).decode()
        print("\n" + instance_xml)
        assert instance_xml is not False
