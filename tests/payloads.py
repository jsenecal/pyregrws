POC_PAYLOAD = \
    """<poc xmlns="http://www.arin.net/regrws/core/v1" >
        <iso3166-1>
            <name>UNITED STATES</name>
            <code2>US</code2>
            <code3>USA</code3>
            <e164>1</e164>
        </iso3166-1>
        <iso3166-2>VA</iso3166-2>
        <emails>
            <email>you@example.com</email>
        </emails>
        <streetAddress>
            <line number = "1">Line 1</line>
            <line number = "2"></line>
            <line number = "3">Line 3</line>
        </streetAddress>
        <city>Chantilly</city>
        <postalCode>20151</postalCode>
        <comment>
            <line number = "1">Line 1</line>
            <line number = "2"></line>
            <line number = "3">Line 3</line>
        </comment>
        <registrationDate>Mon Nov 07 14:04:28 EST 2011</registrationDate>
        <handle>ARIN-HOSTMASTER</handle>
        <contactType>PERSON</contactType>
        <companyName>COMPANYNAME</companyName>
            <firstName>FIRSTNAME</firstName>
        <middleName>MIDDLENAME</middleName>
        <lastName>LASTNAME</lastName>
        <phones>
            <phone>
                <type>
                    <description>DESCRIPTION</description>
                    <code>O</code>
                </type>
                <number>+1.703.227.9840</number>
                <extension>101</extension>
            </phone>
  </phones>
    </poc>"""

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
            <line number = "2"></line>
            <line number = "3">Line 3</line>
        </streetAddress>
        <city>Chantilly</city>
        <iso3166-2>VA</iso3166-2>
        <postalCode>20151</postalCode>
        <comment>
            <line number = "1">Line 1</line>
            <line number = "2"></line>
            <line number = "3">Line 3</line>
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

CUSTOMER_PAYLOAD = """<customer xmlns="http://www.arin.net/regrws/core/v1" >
        <customerName>CUSTOMERNAME</customerName>
        <iso3166-1>
            <name>UNITED STATES</name>
            <code2>US</code2>
            <code3>USA</code3>
            <e164>1</e164>
        </iso3166-1>
        <handle>C1241523</handle>
        <streetAddress>
            <line number = "1">Line 1</line>
            <line number = "2"></line>
            <line number = "3">Line 3</line>
        </streetAddress>
        <city>Chantilly</city>
        <iso3166-2>VA</iso3166-2>
        <postalCode>20151</postalCode>
        <comment>
            <line number = "1">Line 1</line>
            <line number = "2"></line>
            <line number = "3">Line 3</line>
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
            <line number = "2"></line>
            <line number = "3">Line 3</line>
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

ERROR_PAYLOAD = \
    """<error xmlns="http://www.arin.net/regrws/core/v1" >
        <message>MESSAGE</message>
        <code>E_SCHEMA_VALIDATION</code>
        <components>
            <component>
                <name>NAME</name>
                <message>MESSAGE</message>
            </component>
        </components>
        <additionalInfo>
            <message>MESSAGE</message>
        </additionalInfo>
    </error>"""

TICKET_PAYLOAD = \
    """<ticket xmlns="http://www.arin.net/regrws/core/v1"
        xmlns:ns2="http://www.arin.net/regrws/messages/v1"
        xmlns:ns4="http://www.arin.net/regrws/shared-ticket/v1">
        <messages>
            <message>
                <ns2:messageId>MESSAGEID</ns2:messageId>
                <ns2:createdDate>Tue Feb 28 17:41:17 EST 2012</ns2:createdDate>
                <subject>SUBJECT</subject>
                    <text>
                        <line number = "1">Line 1</line>
                        <line number = "2"></line>
                        <line number = "3">Line 3</line>
                    </text>
                <category>NONE</category>
                <attachments>
                    <attachment>
                        <data>DATA</data>
                        <filename>FILENAME</filename>
                    </attachment>
                </attachments>
            </message>
        </messages>
        <ticketNo>TICKETNO</ticketNo>
        <createdDate>Tue Jan 25 16:17:18 EST 2011</createdDate>
        <resolvedDate>Tue Jan 25 16:17:18 EST 2011</resolvedDate>
        <closedDate>Tue Jan 25 16:17:18 EST 2011</closedDate>
        <updatedDate>Tue Jan 25 16:17:18 EST 2011</updatedDate>
        <webTicketType>POC_RECOVERY</webTicketType>
        <webTicketStatus>PENDING_CONFIRMATION</webTicketStatus>
        <webTicketResolution>ACCEPTED</webTicketResolution>
    </ticket>"""

TICKETED_REQUEST_PAYLOAD = \
    f"""<ticketedRequest xmlns="http://www.arin.net/regrws/core/v1">
        {TICKET_PAYLOAD}
        {NET_PAYLOAD}
    </ticketedRequest>"""