# coding: utf-8

"""
    Opportify Insights API

    ## Overview  The **Opportify Insights API** provides access to a powerful and up-to-date platform. With advanced data warehousing and AI-driven capabilities, this API is designed to empower your business to make informed, data-driven decisions and effectively assess potential risks.  ### Base URL Use the following base URL for all API requests:  ```plaintext https://api.opportify.ai/insights/v1/<service>/<endpoint> ```  ### Features - [**Email Insights:**](/docs/api-reference/email-insights)   - Validate email syntax.   - Identify email types (free, disposable, corporate or unknown).   - Real time verifications:     - Reachable: Confirms if the email domain has valid MX DNS records using DNS lookup.     - Deliverable: Simulates an SMTP handshake to check if the email address exists and is deliverable.     - Catch-All: Detects if the domain accepts all emails (catch-all configuration).   - Intelligent Error Correction: Automatically corrects well-known misspelled email addresses.   - Risk Report: Provides an AI-driven normalized score (200-1000) to evaluate email risk, using predefined thresholds.      [Access Documentation >>](/docs/api-reference/email-insights)  - [**IP Insights:**](/docs/api-reference/ip-insights)   - Connection types: Detects connection types such as `wired`, `mobile`, `enterprise`, `satellite`, `VPN`, `cloud-provider`, `open-proxy`, or `Tor`.   - Geo location: Delivers detailed insights such as country, city, timezone, language preferences, and additional location-based information to enhance regional understanding.   - WHOIS: Provides main details including RIR, ASN, organization, and abuse/admin/technical contacts.   - Trusted Provider Recognition: Identifies if the IP is part of a known trusted provider (e.g., ZTNA - Zero Trust Network Access).   - Blocklist Reports: Retrieves up-to-date blocklist statuses, active reports, and the latest detections.   - Risk Report: Delivers an AI-driven normalized score (200-1000) to evaluate IP risk, supported by predefined thresholds.    [Access Documentation >>](/docs/api-reference/ip-insights)  ### Authentication & Security - **API Key:** Access to the API requires an API key, which must be included in the request headers. Businesses can generate unlimited API keys directly from their account, offering flexibility and ease of use.  - **ACL Rules:** Enhance security with Access Control Lists (ACL), allowing you to restrict API access from specific IP addresses or ranges. This feature provides an additional layer of protection by ensuring only authorized IPs can interact with the API. - **No Query Parameters:** As a precautionary measure, our API avoids the use of query parameters for all operations, including authentication and handling Personally Identifiable Information (PII). This approach minimizes security risks by preventing sensitive data from being exposed in access logs, browser history, cached URLs, debugging tools, or inadvertently shared URLs. All sensitive information is securely transmitted through headers or the request body. 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from openapi_client.models.invalidplan import INVALIDPLAN
from openapi_client.models.invalidtoken import INVALIDTOKEN
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

ANALYZEEMAIL403RESPONSEERROR_ONE_OF_SCHEMAS = ["INVALIDPLAN", "INVALIDTOKEN"]

class AnalyzeEmail403ResponseError(BaseModel):
    """
    AnalyzeEmail403ResponseError
    """
    # data type: INVALIDPLAN
    oneof_schema_1_validator: Optional[INVALIDPLAN] = None
    # data type: INVALIDTOKEN
    oneof_schema_2_validator: Optional[INVALIDTOKEN] = None
    actual_instance: Optional[Union[INVALIDPLAN, INVALIDTOKEN]] = None
    one_of_schemas: Set[str] = { "INVALIDPLAN", "INVALIDTOKEN" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = AnalyzeEmail403ResponseError.model_construct()
        error_messages = []
        match = 0
        # validate data type: INVALIDPLAN
        if not isinstance(v, INVALIDPLAN):
            error_messages.append(f"Error! Input type `{type(v)}` is not `INVALIDPLAN`")
        else:
            match += 1
        # validate data type: INVALIDTOKEN
        if not isinstance(v, INVALIDTOKEN):
            error_messages.append(f"Error! Input type `{type(v)}` is not `INVALIDTOKEN`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in AnalyzeEmail403ResponseError with oneOf schemas: INVALIDPLAN, INVALIDTOKEN. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in AnalyzeEmail403ResponseError with oneOf schemas: INVALIDPLAN, INVALIDTOKEN. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into INVALIDPLAN
        try:
            instance.actual_instance = INVALIDPLAN.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into INVALIDTOKEN
        try:
            instance.actual_instance = INVALIDTOKEN.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into AnalyzeEmail403ResponseError with oneOf schemas: INVALIDPLAN, INVALIDTOKEN. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into AnalyzeEmail403ResponseError with oneOf schemas: INVALIDPLAN, INVALIDTOKEN. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], INVALIDPLAN, INVALIDTOKEN]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


