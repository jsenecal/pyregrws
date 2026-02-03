import pytest

from regrws.models import Customer, Error, Org, Poc
from regrws.models.nested import Iso31661
from regrws.models.net import Net, NetBlock
from regrws.models.tickets import TicketRequest

from .payloads import (
    CUSTOMER_PAYLOAD,
    ERROR_EMPTY_COMPONENTS_PAYLOAD,
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


class TestErrorEmptyComponents:
    """Test that Error parses correctly when components is empty.

    ARIN returns <components/> (empty) for some errors, e.g. E_AUTHENTICATION.
    See https://github.com/jsenecal/pyregrws/issues/95
    """

    def test_from_xml(self, cov):
        error = Error.from_xml(ERROR_EMPTY_COMPONENTS_PAYLOAD)
        assert error.code == "E_AUTHENTICATION"
        assert error.message == "The API key is not authorized to make that request."
        assert error.components == []
        assert error.additional_info == []


class TestIso31661:
    """Test that Iso31661 fields are optional per ARIN country payload spec.

    Per https://www.arin.net/resources/manage/regrws/payloads/#country-payload:
    - name and e164 are not required
    - Either code2 or code3 must be specified
    """

    def test_code2_only(self, cov):
        country = Iso31661(code2="US")
        assert country.code2 == "US"
        assert country.name is None
        assert country.code3 is None
        assert country.e164 is None

    def test_code3_only(self, cov):
        country = Iso31661(code3="USA")
        assert country.code3 == "USA"
        assert country.name is None
        assert country.code2 is None
        assert country.e164 is None

    def test_all_fields(self, cov):
        country = Iso31661(name="UNITED STATES", code2="US", code3="USA", e164=1)
        assert country.name == "UNITED STATES"
        assert country.code2 == "US"
        assert country.code3 == "USA"
        assert country.e164 == 1

    def test_code2_and_code3(self, cov):
        country = Iso31661(code2="US", code3="USA")
        assert country.code2 == "US"
        assert country.code3 == "USA"

    def test_no_code_raises(self, cov):
        with pytest.raises(Exception, match="Either code2 or code3 must be specified"):
            Iso31661(name="UNITED STATES")

    def test_xml_roundtrip_code2_only(self, cov):
        xml = '<iso3166-1 xmlns="http://www.arin.net/regrws/core/v1"><code2>US</code2></iso3166-1>'
        country = Iso31661.from_xml(xml)
        assert country.code2 == "US"
        assert country.name is None
        assert country.code3 is None
        assert country.e164 is None
