from __future__ import annotations

from typing import Any, Dict, Optional, List
from pathlib import Path
import json

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

    def batch_analyze(self, params: Dict[str, Any], *, content_type: str = "application/json") -> Dict[str, Any]:
        """Submit a batch IP analysis job.

        Supports:
          - application/json (default): expects 'ips' list
          - multipart/form-data: expects 'file' path containing IPs (one per line or CSV); optional name/enableAi
          - text/plain: expects 'text' raw newline separated IPs OR 'ips' list
        """
        self._refresh_api_instance()
        ct = content_type.lower()
        if ct == "application/json":
            norm = self._normalize_batch_request(params)
            request_body = BatchAnalyzeIpsRequest(**norm)
            try:
                result = self.api_instance.batch_analyze_ips(request_body)
                return result.to_dict()
            except ApiException as exc:  # pragma: no cover
                raise Exception(f"API exception: {exc.status} {exc.reason}") from exc
        if ct == "text/plain":
            if "text" in params:
                raw_text = str(params["text"]).strip()
            else:
                if "ips" not in params:
                    raise ValueError("'ips' or 'text' is required for text/plain submission")
                ips = params["ips"]
                if not isinstance(ips, list):
                    raise ValueError("'ips' must be a list when deriving text body")
                raw_text = "\n".join(str(i).strip() for i in ips if i)
            api_client: ApiClient = self.api_instance.api_client  # type: ignore[assignment]
            method, url, headers, body, post_params = api_client.param_serialize(
                method="POST",
                resource_path="/ip/batch",
                path_params={},
                query_params=[],
                header_params={"Content-Type": "text/plain", "Accept": "application/json"},
                body=raw_text,
                post_params=[],
                files={},
                auth_settings=["opportifyToken"],
                collection_formats={},
                _host=None,
                _request_auth=None,
            )
            response = api_client.call_api(method, url, headers, body, post_params)
            response.read()
            return api_client.response_deserialize(
                response_data=response,
                response_types_map={
                    "202": "BatchAnalyzeIps202Response",
                    "400": "BatchAnalyzeIps400Response",
                    "401": "BatchAnalyzeIps401Response",
                    "402": "BatchAnalyzeIps402Response",
                    "403": "BatchAnalyzeIps403Response",
                    "413": "BatchAnalyzeIps413Response",
                    "429": "BatchAnalyzeIps429Response",
                    "500": "AnalyzeEmail500Response",
                },
            ).data.to_dict()
        if ct == "multipart/form-data":
            if "file" not in params:
                raise ValueError("'file' parameter is required for multipart/form-data")
            return self._batch_analyze_file_multipart(params)
        raise ValueError(f"Unsupported content_type: {content_type}")

    def batch_analyze_file(self, file_path: str, **options: Any) -> Dict[str, Any]:
        params = {"file": file_path, **options}
        return self.batch_analyze(params, content_type="multipart/form-data")

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

    def _batch_analyze_file_multipart(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._refresh_api_instance()
        file_path = Path(str(params["file"]))
        if not file_path.is_file():
            raise ValueError(f"File does not exist: {file_path}")
        enable_ai = params.get("enable_ai") or params.get("enableAi")
        name = params.get("name")
        with file_path.open("rb") as fh:
            file_content = fh.read()
        fields: List[tuple] = [("file", (file_path.name, file_content))]
        if enable_ai is not None:
            fields.append(("enable_ai", "true" if bool(enable_ai) else "false"))
        if name is not None:
            fields.append(("name", str(name)))
        api_client: ApiClient = self.api_instance.api_client  # type: ignore[assignment]
        token = self.config.get_api_key_with_prefix("opportifyToken")
        headers = {"Accept": "application/json"}
        if token:
            headers["x-opportify-token"] = token
        response = api_client.rest_client.pool_manager.request(
            "POST",
            f"{self._final_url}/ip/batch",
            fields=fields,
            encode_multipart=True,
            headers=headers,
            preload_content=False,
        )
        data = response.data
        status = response.status
        text = data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else str(data)
        if status < 200 or status > 299 and status != 202:
            raise Exception(f"API exception: {status} {response.reason}: {text}")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            raise Exception("Unexpected non-JSON response from IP batch file upload")
        return parsed

