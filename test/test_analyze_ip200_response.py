# coding: utf-8

"""
    Opportify Insights API

    ## Overview  The **Opportify Insights API** provides access to a powerful and up-to-date platform. With advanced data warehousing and AI-driven capabilities, this API is designed to empower your business to make informed, data-driven decisions and effectively assess potential risks.  ### Base URL Use the following base URL for all API requests:  ```plaintext https://api.opportify.ai/insights/v1/<service>/<endpoint> ```  ### Features - [**Email Insights:**](/docs/api-reference/email-insights)   - Validate email syntax.   - Identify email types (free, disposable, corporate or unknown).   - Real time verifications:     - Reachable: Confirms if the email domain has valid MX DNS records using DNS lookup.     - Deliverable: Simulates an SMTP handshake to check if the email address exists and is deliverable.     - Catch-All: Detects if the domain accepts all emails (catch-all configuration).   - Intelligent Error Correction: Automatically corrects well-known misspelled email addresses.   - Risk Report: Provides an AI-driven normalized score (200-1000) to evaluate email risk, using predefined thresholds.      [Access Documentation >>](/docs/api-reference/email-insights)  - [**IP Insights:**](/docs/api-reference/ip-insights)   - Connection types: Detects connection types such as `wired`, `mobile`, `enterprise`, `satellite`, `VPN`, `cloud-provider`, `open-proxy`, or `Tor`.   - Geo location: Delivers detailed insights such as country, city, timezone, language preferences, and additional location-based information to enhance regional understanding.   - WHOIS: Provides main details including RIR, ASN, organization, and abuse/admin/technical contacts.   - Trusted Provider Recognition: Identifies if the IP is part of a known trusted provider (e.g., ZTNA - Zero Trust Network Access).   - Blocklist Reports: Retrieves up-to-date blocklist statuses, active reports, and the latest detections.   - Risk Report: Delivers an AI-driven normalized score (200-1000) to evaluate IP risk, supported by predefined thresholds.    [Access Documentation >>](/docs/api-reference/ip-insights)  ### Authentication & Security - **API Key:** Access to the API requires an API key, which must be included in the request headers. Businesses can generate unlimited API keys directly from their account, offering flexibility and ease of use.  - **ACL Rules:** Enhance security with Access Control Lists (ACL), allowing you to restrict API access from specific IP addresses or ranges. This feature provides an additional layer of protection by ensuring only authorized IPs can interact with the API. - **No Query Parameters:** As a precautionary measure, our API avoids the use of query parameters for all operations, including authentication and handling Personally Identifiable Information (PII). This approach minimizes security risks by preventing sensitive data from being exposed in access logs, browser history, cached URLs, debugging tools, or inadvertently shared URLs. All sensitive information is securely transmitted through headers or the request body. 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.analyze_ip200_response import AnalyzeIp200Response

class TestAnalyzeIp200Response(unittest.TestCase):
    """AnalyzeIp200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AnalyzeIp200Response:
        """Test AnalyzeIp200Response
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AnalyzeIp200Response`
        """
        model = AnalyzeIp200Response()
        if include_optional:
            return AnalyzeIp200Response(
                ip_address = '192.168.0.1',
                ip_address_number = 3232235521,
                ip_type = 'IPv4',
                ip_cidr = '192.168.0.0/24',
                connection_type = 'wired',
                host_reverse = '10.184.114.89.rev.providerhost.com',
                geo = openapi_client.models.geo.Geo(
                    continent = 'North America', 
                    country_code = 'US', 
                    country_name = 'United States of America', 
                    country_short_name = 'United States', 
                    city = 'San Francisco', 
                    currency_code = 'USD', 
                    domain_extension = '.com', 
                    languages = 'en-US, es-US, es', 
                    latitude = 37.7749, 
                    longitude = -122.4194, 
                    postal_code = '94105', 
                    phone_int_code = '1', 
                    region = 'California', 
                    timezone = 'America/Los_Angeles', ),
                whois = openapi_client.models.whois.Whois(
                    rir = 'ARIN', 
                    asn = openapi_client.models.asn.Asn(
                        asn_id = '15169', 
                        as_name = 'GOOGLE', 
                        descr = ["Google LLC","Mountain View, CA"], 
                        email = ["asn-email@somedomain.com"], ), 
                    organization = openapi_client.models.organization.Organization(
                        org_id = 'GOOGL', 
                        org_name = 'Google LLC', 
                        org_type = 'ISP', 
                        descr = ["Leading internet provider","Mountain View, CA"], 
                        address = ["1600 Amphitheatre Parkway"], 
                        country = 'US', 
                        phone = ["+1-800-555-1234"], 
                        fax = ["+1-800-555-5678"], 
                        email = ["support@organization.com"], ), 
                    abuse_contact = openapi_client.models.abuse_contact.AbuseContact(
                        contact_id = 'ABUSE123', 
                        contact_type = 'abuse', 
                        name = 'Abuse Desk', 
                        address = ["123 Abuse St, Suite 100"], 
                        phone = ["+1-800-ABUSE-123"], 
                        fax = ["+1-800-ABUSE-456"], 
                        email = ["abuse@organization.com"], ), 
                    admin_contact = openapi_client.models.admin_contact.AdminContact(
                        contact_id = 'ADMIN123', 
                        contact_type = 'admin', 
                        name = 'Admin Desk', 
                        address = ["456 Admin Lane"], 
                        phone = ["+1-800-ADMIN-123"], 
                        fax = ["+1-800-ADMIN-456"], 
                        email = ["admin@organization.com"], ), 
                    tech_contact = openapi_client.models.tech_contact.TechContact(
                        contact_id = 'TECH123', 
                        contact_type = 'tech', 
                        name = 'Tech Desk', 
                        address = ["456 Tech Lane"], 
                        phone = ["+1-800-TECH-123"], 
                        fax = ["+1-800-TECH-456"], 
                        email = ["tech@organization.com"], ), ),
                trusted_provider = openapi_client.models.trusted_provider.TrustedProvider(
                    is_known_provider = True, 
                    provider = 'ZScaler', 
                    provider_type = 'ZTNE', 
                    description = 'Zero Trust Network Access for Enterprises', ),
                blocklisted = openapi_client.models.block_listed.BlockListed(
                    is_block_listed = False, 
                    sources = 0, 
                    active_reports = 0, 
                    last_detected = '2022-01-01T12:00Z', ),
                risk_report = openapi_client.models.risk_report.RiskReport(
                    score = 850, 
                    level = 'highest', )
            )
        else:
            return AnalyzeIp200Response(
                ip_address = '192.168.0.1',
                ip_address_number = 3232235521,
                ip_type = 'IPv4',
                ip_cidr = '192.168.0.0/24',
                connection_type = 'wired',
                host_reverse = '10.184.114.89.rev.providerhost.com',
                geo = openapi_client.models.geo.Geo(
                    continent = 'North America', 
                    country_code = 'US', 
                    country_name = 'United States of America', 
                    country_short_name = 'United States', 
                    city = 'San Francisco', 
                    currency_code = 'USD', 
                    domain_extension = '.com', 
                    languages = 'en-US, es-US, es', 
                    latitude = 37.7749, 
                    longitude = -122.4194, 
                    postal_code = '94105', 
                    phone_int_code = '1', 
                    region = 'California', 
                    timezone = 'America/Los_Angeles', ),
                whois = openapi_client.models.whois.Whois(
                    rir = 'ARIN', 
                    asn = openapi_client.models.asn.Asn(
                        asn_id = '15169', 
                        as_name = 'GOOGLE', 
                        descr = ["Google LLC","Mountain View, CA"], 
                        email = ["asn-email@somedomain.com"], ), 
                    organization = openapi_client.models.organization.Organization(
                        org_id = 'GOOGL', 
                        org_name = 'Google LLC', 
                        org_type = 'ISP', 
                        descr = ["Leading internet provider","Mountain View, CA"], 
                        address = ["1600 Amphitheatre Parkway"], 
                        country = 'US', 
                        phone = ["+1-800-555-1234"], 
                        fax = ["+1-800-555-5678"], 
                        email = ["support@organization.com"], ), 
                    abuse_contact = openapi_client.models.abuse_contact.AbuseContact(
                        contact_id = 'ABUSE123', 
                        contact_type = 'abuse', 
                        name = 'Abuse Desk', 
                        address = ["123 Abuse St, Suite 100"], 
                        phone = ["+1-800-ABUSE-123"], 
                        fax = ["+1-800-ABUSE-456"], 
                        email = ["abuse@organization.com"], ), 
                    admin_contact = openapi_client.models.admin_contact.AdminContact(
                        contact_id = 'ADMIN123', 
                        contact_type = 'admin', 
                        name = 'Admin Desk', 
                        address = ["456 Admin Lane"], 
                        phone = ["+1-800-ADMIN-123"], 
                        fax = ["+1-800-ADMIN-456"], 
                        email = ["admin@organization.com"], ), 
                    tech_contact = openapi_client.models.tech_contact.TechContact(
                        contact_id = 'TECH123', 
                        contact_type = 'tech', 
                        name = 'Tech Desk', 
                        address = ["456 Tech Lane"], 
                        phone = ["+1-800-TECH-123"], 
                        fax = ["+1-800-TECH-456"], 
                        email = ["tech@organization.com"], ), ),
                trusted_provider = openapi_client.models.trusted_provider.TrustedProvider(
                    is_known_provider = True, 
                    provider = 'ZScaler', 
                    provider_type = 'ZTNE', 
                    description = 'Zero Trust Network Access for Enterprises', ),
                blocklisted = openapi_client.models.block_listed.BlockListed(
                    is_block_listed = False, 
                    sources = 0, 
                    active_reports = 0, 
                    last_detected = '2022-01-01T12:00Z', ),
                risk_report = openapi_client.models.risk_report.RiskReport(
                    score = 850, 
                    level = 'highest', ),
        )
        """

    def testAnalyzeIp200Response(self):
        """Test AnalyzeIp200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()