"""Test for Net model with empty pocLinks tag - Issue #43"""

from regrws.models.net import Net


def test_net_with_empty_poclinks():
    """Test that Net model can handle empty pocLinks tags from ARIN API

    This test reproduces the issue reported in #43 where the API returns
    an empty <pocLinks/> tag which causes a validation error.
    """
    # This is the actual XML response that causes the crash
    # as reported in issue #43
    xml_payload = """<net xmlns="http://www.arin.net/regrws/core/v1">
        <version>4</version>
        <registrationDate>Tue Jan 25 16:17:18 EST 2011</registrationDate>
        <handle>NET-204-62-56-0-1</handle>
        <netBlocks>
            <netBlock>
                <type>A</type>
                <description>Direct Allocation</description>
                <startAddress>204.062.056.000</startAddress>
                <endAddress>204.062.063.255</endAddress>
                <cidrLength>21</cidrLength>
            </netBlock>
        </netBlocks>
        <orgHandle>EXAMPLE-ORG</orgHandle>
        <netName>EXAMPLE-NET</netName>
        <pocLinks/>
    </net>"""

    # This should not raise a validation error
    net = Net.from_xml(xml_payload)

    # Verify the net was parsed correctly
    assert net.handle == "NET-204-62-56-0-1"
    assert net.version.value == 4
    assert net.org_handle == "EXAMPLE-ORG"
    assert net.net_name == "EXAMPLE-NET"

    # poc_links should be an empty list, not None
    assert net.poc_links is not None
    assert len(net.poc_links) == 0
    assert net.poc_links == []
