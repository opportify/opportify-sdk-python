from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from openapi_client.configuration import Configuration as ApiConfiguration
from openapi_client.api_client import ApiClient
from openapi_client.api.email_insights_api import EmailInsightsApi
from openapi_client.models.analyze_email_request import AnalyzeEmailRequest
from openapi_client.models.batch_analyze_emails_request import BatchAnalyzeEmailsRequest
from openapi_client.exceptions import ApiException


class EmailInsights:

    def __init__(
        self,
        api_key: str,
        api_instance: Optional[EmailInsightsApi] = None,
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
        # openapi generator expects the security scheme key name
        self.config.api_key = {"opportifyToken": api_key}

        # Allow injection for tests; if provided we'll still update its api_client.host later
        self.api_instance: Optional[EmailInsightsApi] = api_instance
        if api_instance is None:
            self._refresh_api_instance(first_run=True)
        else:
            # Ensure the injected instance uses the composed host
            self.api_instance.api_client.configuration.host = self._final_url

    # ---------------------------------------------------------------------
    # Public configuration mutators
    # ---------------------------------------------------------------------
    def set_host(self, host: str) -> "EmailInsights":
        host = host.rstrip("/")
        if host != self._host:
            self._host = host
            self._mark_config_changed()
        return self

    def set_version(self, version: str) -> "EmailInsights":
        version = version.strip("/")
        if version != self._version:
            self._version = version
            self._mark_config_changed()
        return self

    def set_prefix(self, prefix: str) -> "EmailInsights":
        prefix = prefix.strip("/")
        if prefix != self._prefix:
            self._prefix = prefix
            self._mark_config_changed()
        return self

    def set_debug_mode(self, debug_mode: bool) -> "EmailInsights":
        if debug_mode != self._debug_mode:
            self._debug_mode = debug_mode
            self._mark_config_changed()
        return self

    # ---------------------------------------------------------------------
    # Core endpoint wrappers
    # ---------------------------------------------------------------------
    def analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single email address.

        Parameters
        ----------
        params: dict
            Required: email (str). Optional: enable_ai / enableAi,
            enable_auto_correction / enableAutoCorrection.
        """
        self._refresh_api_instance()
        norm = self._normalize_request(params)
        request_body = AnalyzeEmailRequest(**norm)
        try:
            result = self.api_instance.analyze_email(request_body)
            return result.to_dict()
        except ApiException as exc:  # pragma: no cover - simple passthrough
            raise Exception(f"API exception: {exc.status} {exc.reason}") from exc

    def batch_analyze(
        self,
        params: Dict[str, Any],
        *,
        content_type: str = "application/json",
    ) -> Dict[str, Any]:
        """Submit a batch of emails for asynchronous analysis.

        Supports three content types:
          - application/json (default): expects 'emails' list and optional flags
          - multipart/form-data: expects 'file' (path), optional enable_ai/enable_auto_correction/name
          - text/plain: expects 'text' (newline separated emails) or 'emails' list
        """
        self._refresh_api_instance()
        ct = content_type.lower()

        if ct == "application/json":
            normalized = self._normalize_batch_request(params)
            body = BatchAnalyzeEmailsRequest(**normalized)
            try:
                result = self.api_instance.batch_analyze_emails(body)
                return result.to_dict()  # type: ignore[attr-defined]
            except ApiException as exc:  # pragma: no cover
                raise Exception(f"API exception: {exc.status} {exc.reason}") from exc

        if ct == "text/plain":
            # Accept either raw 'text' or build from emails list
            if "text" in params:
                raw_text = str(params["text"]).strip()
            else:
                if "emails" not in params:
                    raise ValueError("'emails' or 'text' is required for text/plain batch submission")
                emails = params["emails"]
                if not isinstance(emails, list):
                    raise ValueError("'emails' must be a list when using application/json or text aggregation")
                raw_text = "\n".join(str(e).strip() for e in emails if e)
            # We bypass the generated helper to supply raw text body
            api_client: ApiClient = self.api_instance.api_client  # type: ignore[assignment]
            method, url, headers, body, post_params = api_client.param_serialize(
                method="POST",
                resource_path="/email/batch",
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
                    "202": "BatchAnalyzeEmails202Response",
                    "400": "BatchAnalyzeEmails400Response",
                    "401": "BatchAnalyzeEmails401Response",
                    "402": "BatchAnalyzeEmails402Response",
                    "403": "BatchAnalyzeEmails403Response",
                    "413": "BatchAnalyzeEmails413Response",
                    "429": "BatchAnalyzeEmails429Response",
                    "500": "AnalyzeEmail500Response",
                },
            ).data.to_dict()

        if ct == "multipart/form-data":
            if "file" not in params:
                raise ValueError("'file' parameter (path) is required for multipart/form-data")
            return self._batch_analyze_file_multipart(params)

        raise ValueError(f"Unsupported content_type: {content_type}")

    def batch_analyze_file(self, file_path: str, **options: Any) -> Dict[str, Any]:
        """Convenience helper to submit a file path as multipart/form-data.

        Parameters
        ----------
        file_path: str
            Path to a CSV or text file containing emails.
        options: Any
            Optional flags: enable_ai / enableAi, enable_auto_correction / enableAutoCorrection, name.
        """
        params = {"file": file_path, **options}
        return self.batch_analyze(params, content_type="multipart/form-data")

    def get_batch_status(self, job_id: str) -> Dict[str, Any]:
        self._refresh_api_instance()
        try:
            result = self.api_instance.get_email_batch_status(job_id)
            return result.to_dict()
        except ApiException as exc:  # pragma: no cover
            raise Exception(f"API exception: {exc.status} {exc.reason}") from exc

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------
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
        self.api_instance = EmailInsightsApi(api_client)
        self._config_changed = False

    def _normalize_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if "email" not in params:
            raise ValueError("'email' is required")
        normalized: Dict[str, Any] = {"email": str(params["email"])}
        # Map camelCase variants
        if "enableAi" in params and "enable_ai" not in params:
            params["enable_ai"] = params.pop("enableAi")
        if "enableAutoCorrection" in params and "enable_auto_correction" not in params:
            params["enable_auto_correction"] = params.pop("enableAutoCorrection")
        normalized["enable_ai"] = bool(params.get("enable_ai", False))
        normalized["enable_auto_correction"] = bool(params.get("enable_auto_correction", False))
        return normalized

    def _normalize_batch_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        if "emails" not in params or not isinstance(params["emails"], list):
            raise ValueError("'emails' (list) is required for JSON batch submission")
        emails = [str(e) for e in params["emails"] if e]
        if not emails:
            raise ValueError("'emails' list must contain at least one email")
        # Map camelCase
        if "enableAi" in params and "enable_ai" not in params:
            params["enable_ai"] = params.pop("enableAi")
        if "enableAutoCorrection" in params and "enable_auto_correction" not in params:
            params["enable_auto_correction"] = params.pop("enableAutoCorrection")
        out: Dict[str, Any] = {"emails": emails}
        if "name" in params:
            out["name"] = str(params["name"])
        if "enable_ai" in params:
            out["enable_ai"] = bool(params["enable_ai"])
        if "enable_auto_correction" in params:
            out["enable_auto_correction"] = bool(params["enable_auto_correction"])
        return out

    def _batch_analyze_file_multipart(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._refresh_api_instance()
        file_path = Path(str(params["file"]))
        if not file_path.is_file():
            raise ValueError(f"File does not exist: {file_path}")
        enable_ai = params.get("enable_ai") or params.get("enableAi")
        enable_auto_correction = params.get("enable_auto_correction") or params.get("enableAutoCorrection")
        name = params.get("name")

        # Build multipart parts (field name -> value)
        fields: List[tuple] = []
        # File part
        with file_path.open("rb") as fh:
            file_content = fh.read()
        fields.append(("file", (file_path.name, file_content)))  # type: ignore[arg-type]
        if enable_ai is not None:
            fields.append(("enable_ai", "true" if bool(enable_ai) else "false"))
        if enable_auto_correction is not None:
            fields.append(("enable_auto_correction", "true" if bool(enable_auto_correction) else "false"))
        if name is not None:
            fields.append(("name", str(name)))

        # Manually construct multipart using underlying rest client (urllib3 handles boundary)
        api_client: ApiClient = self.api_instance.api_client  # type: ignore[assignment]
        # We can't easily re-use param_serialize for multipart because the generator uses model body.
        # Instead we perform a direct request here.
        token = self.config.get_api_key_with_prefix("opportifyToken")
        headers = {"Accept": "application/json"}
        if token:
            headers["x-opportify-token"] = token
        response = api_client.rest_client.pool_manager.request(
            "POST",
            f"{self._final_url}/email/batch",
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
            raise Exception("Unexpected non-JSON response from batch file upload")
        return parsed

