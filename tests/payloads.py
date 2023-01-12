ORG_PAYLOAD = \
    """<org xmlns="http://www.arin.net/regrws/core/v1" >
        <iso3166-1>
            <name>UNITED STATES</name>
            <code2>US</code2>
            <code3>USA</code3>
            <e164>1</e164>
        </iso3166-1>
        <streetAddress>
            <line number = "1">Line 1</line>
        </streetAddress>
        <city>Chantilly</city>
        <iso3166-2>VA</iso3166-2>
        <postalCode>20151</postalCode>
        <comment>
            <line number = "1">Line 1</line>
        </comment>
        <handle>ARIN</handle>
        <registrationDate>Mon Nov 07 14:04:28 EST 2011</registrationDate>
        <orgName>ORGNAME</orgName>
        <dbaName>DBANAME</dbaName>
        <taxId>TAXID</taxId>
        <orgUrl>http://example.com/org/ARIN</orgUrl>
        <pocLinks>
            <pocLinkRef description="Tech" function="T" handle="EXAMPLETECH-ARIN"/>
            <pocLinkRef description="Admin" function="AD" handle="EXAMPLEADMIN-ARIN"/>
        </pocLinks>
    </org>"""

CUSTOMER_PAYLOAD = \
    """<customer xmlns="http://www.arin.net/regrws/core/v1" >
        <customerName>CUSTOMERNAME</customerName>
        <iso3166-1>
            <name>UNITED STATES</name>
            <code2>US</code2>
            <code3>USA</code3>
            <e164>1</e164>
        </iso3166-1>
        <streetAddress>
            <line number = "1">Line 1</line>
        </streetAddress>
        <city>Chantilly</city>
            <iso3166-2>VA</iso3166-2>
        <postalCode>20151</postalCode>
        <comment>
            <line number = "1">Line 1</line>
        </comment>
        <handle>CUST</handle>
        <parentOrgHandle>PARENTORGHANDLE</parentOrgHandle>
        <registrationDate>Mon Nov 07 14:04:28 EST 2011</registrationDate>
        <privateCustomer>false</privateCustomer>
    </customer>"""

NETBLOCK_PAYLOAD = \
    """<netBlock xmlns="http://www.arin.net/regrws/core/v1" >
        <type>A</type>
        <description>DESCRIPTION</description>
        <startAddress>010.000.000.000</startAddress>
        <endAddress>010.000.000.255</endAddress>
        <cidrLength>24</cidrLength>
    </netBlock>"""

NET_PAYLOAD = \
    """<net xmlns="http://www.arin.net/regrws/core/v1" >
        <version>4</version>
        <comment>
            <line number = "1">Line 1</line>
        </comment>
        <registrationDate>Tue Jan 25 16:17:18 EST 2011</registrationDate>
        <handle>NET-10-0-0-0-1</handle>
        <netBlocks>
            <netBlock>
                <type>A</type>
                <description>DESCRIPTION</description>
                <startAddress>010.000.000.000</startAddress>
                <endAddress>010.000.000.255</endAddress>
                <cidrLength>24</cidrLength>
            </netBlock>
        </netBlocks>
        <customerHandle>C12341234</customerHandle>
        <parentNetHandle>PARENTNETHANDLE</parentNetHandle>
        <netName>NETNAME</netName>
        <originASes>
            <originAS>AS102</originAS>
        </originASes>
        <pocLinks>
            <pocLinkRef description="Tech" function="T" handle="EXAMPLETECH-ARIN"/>
            <pocLinkRef description="Admin" function="AD" handle="EXAMPLEADMIN-ARIN"/>
        </pocLinks>
    </net>"""