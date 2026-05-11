# Auto-generated skeleton. Review and implement each method.
from typing import Optional, Dict, Any
from fraud_intel_client.configuration import Configuration as ApiConfiguration
from fraud_intel_client.api_client import ApiClient
from fraud_intel_client.api.fraud_protection_api import FraudProtectionApi
from fraud_intel_client.exceptions import ApiException


class FraudProtection:
    def __init__(self, api_key: str, api_instance: Optional[FraudProtectionApi] = None):
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
        if not self.config_changed and not first_run:
            return
        self._update_final_url()
        self.config.host = self.final_url
        api_client = ApiClient(configuration=self.config)
        api_client.configuration.debug = self.debug_mode
        self.api_instance = FraudProtectionApi(api_client)
        self.config_changed = False

    def _update_final_url(self) -> None:
        base = self.host.rstrip('/')
        segments = [s for s in [self.prefix.strip('/'), self.version.strip('/')] if s]
        self.final_url = base + ('/' + '/'.join(segments) if segments else '')

    def set_host(self, host: str) -> None: self.host = host; self.config_changed = True
    def set_version(self, version: str) -> None: self.version = version; self.config_changed = True
    def set_prefix(self, prefix: str) -> None: self.prefix = prefix; self.config_changed = True
    def set_debug_mode(self, debug: bool) -> None: self.debug_mode = debug; self.config_changed = True

    def analyze_fraud(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze

        :param params: Request parameters.
        :return: Response as dictionary.
        """
        self._refresh_api_instance()
        raise NotImplementedError("analyze_fraud is not yet implemented.")
