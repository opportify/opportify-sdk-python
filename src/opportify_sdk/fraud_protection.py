# src/fraud_protection.py
from typing import Optional, Dict, Any, List
from fraud_intel_client.configuration import Configuration as ApiConfiguration
from fraud_intel_client.api_client import ApiClient
from fraud_intel_client.api.fraud_protection_api import FraudProtectionApi
from fraud_intel_client.models.analyze_fraud_request import AnalyzeFraudRequest



class FraudProtection:
    def __init__(self, api_key: str, api_instance: Optional[FraudProtectionApi] = None):
        """
        Initialize the FraudProtection class with the provided API key.

        :param api_key: The API key for authentication.
        :param api_instance: Optional API instance for testing purposes.
        """
        self.config = ApiConfiguration()
        self.config.api_key = {"opportifyToken": api_key}
        self.host = "https://api.opportify.ai"
        self.prefix = "intel"
        self.version = "v1"
        self.debug_mode = False
        self.final_url = ""
        self.config_changed = False

        self._update_final_url()

        if api_instance:
            self.api_instance = api_instance
        else:
            self._refresh_api_instance(first_run=True)

    def _refresh_api_instance(self, first_run: bool = False) -> None:
        """
        Ensures API instance is updated only if config has changed.

        :param first_run: Whether this is the first initialization.
        """
        if not self.config_changed and not first_run:
            return

        self._update_final_url()
        self.config.host = self.final_url
        api_client = ApiClient(configuration=self.config)
        api_client.configuration.debug = self.debug_mode
        self.api_instance = FraudProtectionApi(api_client)
        self.config_changed = False

    def _update_final_url(self) -> None:
        """
        Updates the final URL used for API requests.
        """
        base = self.host.rstrip('/')
        segments = []

        prefix = self.prefix.strip('/')
        if prefix:
            segments.append(prefix)

        version = self.version.strip('/')
        if version:
            segments.append(version)

        self.final_url = base + ('/' + '/'.join(segments) if segments else '')

    def analyze_fraud(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a synchronous multi-signal fraud risk assessment on a form submission.

        At least one of ``email`` or ``userIp`` / ``user_ip`` is required.

        :param params: Dictionary containing submission fields for fraud analysis.
            Required (at least one):
                - email (str): Email address associated with the submission.
                - userIp / user_ip (str): IPv4 or IPv6 address of the submitting user.
            Optional:
                - phone1 (str): Primary phone number in E.164 format.
                - phone2 (str): Secondary phone number in E.164 format.
                - firstName / first_name (str): First name of the submitter.
                - lastName / last_name (str): Last name of the submitter.
                - fullName / full_name (str): Full name when first/last are not split.
                - username (str): Requested username or handle.
                - companyName / company_name (str): Company or organization name.
                - website (str): Website URL provided by the submitter.
                - subject (str): Subject line for contact or support forms.
                - message (str): Free-text message body of the submission.
                - address1 (str): Primary street address.
                - address2 (str): Apartment, suite, or unit number.
                - city (str): City of the submitter.
                - region (str): State, province, or region code.
                - country (str): ISO 3166-1 alpha-2 country code.
                - postalCode / postal_code (str): Postal or ZIP code.
                - origin (str): Hostname of the page where the form was submitted.
                - submissionType / submission_type (str): Semantic type of the form.
                - formData / form_data (dict): Arbitrary additional form fields.
                - opportifyToken / opportify_token (str): Token from Opportify frontend SDK.
                - opportifyFormUUID / opportify_form_uuid (str): UUID of the form in the dashboard.
        :return: The fraud risk assessment result as a dictionary.
        :raises ApiException: Propagates directly from the underlying API client if the request fails.
        """
        self._refresh_api_instance()

        normalized = self._normalize_request(params)
        analyze_fraud_request = AnalyzeFraudRequest(**normalized)

        result = self.api_instance.analyze_fraud(analyze_fraud_request)
        return result.to_dict()

    def set_host(self, host: str) -> "FraudProtection":
        """
        Set the host.

        :param host: The host URL.
        :return: The current instance for chaining.
        """
        if self.host != host:
            self.host = host
            self.config_changed = True
        return self

    def set_version(self, version: str) -> "FraudProtection":
        """
        Set the version.

        :param version: The API version.
        :return: The current instance for chaining.
        """
        if self.version != version:
            self.version = version
            self.config_changed = True
        return self

    def set_prefix(self, prefix: str) -> "FraudProtection":
        """
        Set the prefix.

        :param prefix: The URL prefix.
        :return: The current instance for chaining.
        """
        prefix = prefix.strip('/')
        if self.prefix != prefix:
            self.prefix = prefix
            self.config_changed = True
        return self

    def set_debug_mode(self, debug_mode: bool) -> "FraudProtection":
        """
        Set the debug mode.

        :param debug_mode: Enable or disable debug mode.
        :return: The current instance for chaining.
        """
        if self.debug_mode != debug_mode:
            self.debug_mode = debug_mode
            self.config_changed = True
        return self

    def _normalize_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the request parameters, accepting both snake_case and camelCase keys.

        :param params: The raw parameters.
        :return: Normalized parameters using snake_case keys matching AnalyzeFraudRequest fields.
        """
        has_email = 'email' in params and params['email']
        has_user_ip = self._get_first(params, ['user_ip', 'userIp'])

        if not has_email and not has_user_ip:
            raise ValueError("At least one of 'email' or 'userIp' / 'user_ip' is required.")

        normalized: Dict[str, Any] = {}

        if has_email:
            normalized['email'] = str(params['email'])

        user_ip = self._get_first(params, ['user_ip', 'userIp'])
        if user_ip is not None:
            normalized['user_ip'] = str(user_ip)

        for snake, camel in [
            ('phone1', 'phone1'),
            ('phone2', 'phone2'),
            ('first_name', 'firstName'),
            ('last_name', 'lastName'),
            ('full_name', 'fullName'),
            ('username', 'username'),
            ('company_name', 'companyName'),
            ('website', 'website'),
            ('subject', 'subject'),
            ('message', 'message'),
            ('address1', 'address1'),
            ('address2', 'address2'),
            ('city', 'city'),
            ('region', 'region'),
            ('country', 'country'),
            ('postal_code', 'postalCode'),
            ('origin', 'origin'),
            ('submission_type', 'submissionType'),
            ('opportify_token', 'opportifyToken'),
            ('opportify_form_uuid', 'opportifyFormUUID'),
        ]:
            value = self._get_first(params, [snake, camel])
            if value is not None:
                normalized[snake] = str(value)

        form_data = self._get_first(params, ['form_data', 'formData'])
        if form_data is not None:
            if not isinstance(form_data, dict):
                raise ValueError("'formData' / 'form_data' must be a dictionary.")
            normalized['form_data'] = form_data

        return normalized

    def _get_first(self, params: Dict[str, Any], keys: List[str]) -> Any:
        """
        Return the first non-blank value found in params for any of the given keys, or None.

        String values are stripped before checking; blank strings and other falsy values
        are treated as absent so that a later alias key (e.g. camelCase after snake_case)
        can still match. Non-string values use a standard truthy check.

        :param params: The parameters dictionary.
        :param keys: List of keys to check in order.
        :return: First matched non-blank value, or None.
        """
        for key in keys:
            if key in params:
                val = params[key]
                if isinstance(val, str):
                    if val.strip():
                        return val
                elif val:
                    return val
        return None
