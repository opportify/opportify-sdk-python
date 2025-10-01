from __future__ import annotations

from typing import Any, Dict, Optional

from openapi_client.configuration import Configuration as ApiConfiguration
from openapi_client.api_client import ApiClient
from openapi_client.api.ip_insights_api import IPInsightsApi
from openapi_client.models.analyze_ip_request import AnalyzeIpRequest
from openapi_client.models.batch_analyze_ips_request import BatchAnalyzeIpsRequest
from openapi_client.exceptions import ApiException

class IpInsights:
    def __init__(
        self,
        api_key: str,
        api_instance: Optional[IPInsightsApi] = None,
        *,
        host: str = "https://api.opportify.ai",
        prefix: str = "insights",
        version: str = "v1",
    ) -> None:
        self._host = host.rstrip("/")
        self._prefix = prefix.strip("/")
        self._version = version.strip("/")
        self._final_url = self._compose_final_url()
        self._config_changed = True
        self._debug_mode = False

        self.config = ApiConfiguration()
        self.config.api_key = {"opportifyToken": api_key}

        self.api_instance: Optional[IPInsightsApi] = api_instance
        if api_instance is None:
            self._refresh_api_instance(first_run=True)
        else:
            self.api_instance.api_client.configuration.host = self._final_url

    # ------------------------------------------------------------------
    # Public mutators
    # ------------------------------------------------------------------
    def set_host(self, host: str) -> "IpInsights":
        host = host.rstrip("/")
        if host != self._host:
            self._host = host
            self._mark_config_changed()
        return self

    def set_version(self, version: str) -> "IpInsights":
        version = version.strip("/")
        if version != self._version:
            self._version = version
            self._mark_config_changed()
        return self

    def set_prefix(self, prefix: str) -> "IpInsights":
        prefix = prefix.strip("/")
        if prefix != self._prefix:
            self._prefix = prefix
            self._mark_config_changed()
        return self

    def set_debug_mode(self, debug_mode: bool) -> "IpInsights":
        if debug_mode != self._debug_mode:
            self._debug_mode = debug_mode
            self._mark_config_changed()
        return self

    # ------------------------------------------------------------------
    # Endpoint wrappers
    # ------------------------------------------------------------------
    def analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._refresh_api_instance()
        norm = self._normalize_request(params)
        request_body = AnalyzeIpRequest(**norm)
        try:
            result = self.api_instance.analyze_ip(request_body)
            return result.to_dict()
        except ApiException as exc:  # pragma: no cover
            raise Exception(f"API exception: {exc.status} {exc.reason}") from exc

    def batch_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._refresh_api_instance()
        norm = self._normalize_batch_request(params)
        request_body = BatchAnalyzeIpsRequest(**norm)
        try:
            result = self.api_instance.batch_analyze_ips(request_body)
            return result.to_dict()
        except ApiException as exc:  # pragma: no cover
            raise Exception(f"API exception: {exc.status} {exc.reason}") from exc

    def get_batch_status(self, job_id: str) -> Dict[str, Any]:
        self._refresh_api_instance()
        try:
            result = self.api_instance.get_ip_batch_status(job_id)
            return result.to_dict()
        except ApiException as exc:  # pragma: no cover
            raise Exception(f"API exception: {exc.status} {exc.reason}") from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _mark_config_changed(self) -> None:
        self._config_changed = True

    def _compose_final_url(self) -> str:
        segments = [self._host]
        if self._prefix:
            segments.append(self._prefix)
        if self._version:
            segments.append(self._version)
        return "/".join(segments)

    def _refresh_api_instance(self, *, first_run: bool = False) -> None:
        if not self._config_changed and not first_run and self.api_instance is not None:
            return
        self._final_url = self._compose_final_url()
        self.config.host = self._final_url
        api_client = ApiClient(configuration=self.config)
        api_client.configuration.debug = self._debug_mode
        self.api_instance = IPInsightsApi(api_client)
        self._config_changed = False

    def _normalize_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if "ip" not in params:
            raise ValueError("'ip' is required")
        normalized: Dict[str, Any] = {"ip": str(params["ip"]) }
        if "enableAi" in params and "enable_ai" not in params:
            params["enable_ai"] = params.pop("enableAi")
        if "enable_ai" in params:
            normalized["enable_ai"] = bool(params["enable_ai"])
        return normalized

    def _normalize_batch_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if "ips" not in params or not isinstance(params["ips"], list):
            raise ValueError("'ips' (list) is required for batch submission")
        ips = [str(ip) for ip in params["ips"] if ip]
        if not ips:
            raise ValueError("'ips' list must contain at least one ip")
        if "enableAi" in params and "enable_ai" not in params:
            params["enable_ai"] = params.pop("enableAi")
        out: Dict[str, Any] = {"ips": ips}
        if "name" in params:
            out["name"] = str(params["name"])
        if "enable_ai" in params:
            out["enable_ai"] = bool(params["enable_ai"])
        return out

