"""Unit tests for high-level SDK wrappers in `opportify_sdk`.

These tests focus on:
 - Parameter normalization (camelCase to snake_case)
 - Inclusion of optional `name` in batch requests
 - Basic configuration mutation not triggering rebuild when not needed
 - Error handling for missing required params & invalid file paths

Network calls are avoided by injecting / replacing the underlying generated
API instances with light-weight dummies capturing the request bodies.
"""
from __future__ import annotations

import pytest

from opportify_sdk import EmailInsights, IpInsights


class _DummyResult:
    def __init__(self, payload=None):
        self._payload = payload or {"ok": True}

    def to_dict(self):  # pragma: no cover - trivial
        return self._payload


class _DummyEmailApi:
    def __init__(self):
        self.last_analyze_body = None
        self.last_batch_body = None

    # Signatures mirror generated client usage in wrapper
    def analyze_email(self, body):  # pragma: no cover (simple capture)
        self.last_analyze_body = body
        return _DummyResult({"analyze": True})

    def batch_analyze_emails(self, body):  # pragma: no cover
        self.last_batch_body = body
        return _DummyResult({"batch": True})

    def get_email_batch_status(self, job_id):  # pragma: no cover
        return _DummyResult({"jobId": job_id})


class _DummyIpApi:
    def __init__(self):
        self.last_analyze_body = None
        self.last_batch_body = None

    def analyze_ip(self, body):  # pragma: no cover
        self.last_analyze_body = body
        return _DummyResult({"analyzeIp": True})

    def batch_analyze_ips(self, body):  # pragma: no cover
        self.last_batch_body = body
        return _DummyResult({"batchIp": True})

    def get_ip_batch_status(self, job_id):  # pragma: no cover
        return _DummyResult({"jobId": job_id})


# --------------------- EmailInsights tests ---------------------

def _prepare_email_wrapper() -> tuple[EmailInsights, _DummyEmailApi]:
    wrapper = EmailInsights("dummy-key")
    dummy = _DummyEmailApi()
    # Prevent refresh from overwriting our dummy
    wrapper.api_instance = dummy  # type: ignore[attr-defined]
    if hasattr(wrapper, "_config_changed"):
        wrapper._config_changed = False  # type: ignore[attr-defined]
    return wrapper, dummy


def test_email_analyze_normalization():
    wrapper, dummy = _prepare_email_wrapper()
    res = wrapper.analyze({
        "email": "user@example.com",
        "enableAi": True,
        "enableAutoCorrection": False,
    })
    assert res == {"analyze": True}
    assert dummy.last_analyze_body is not None
    body_dict = dummy.last_analyze_body.to_dict()
    # Expect alias keys per model definitions
    assert body_dict["email"] == "user@example.com"
    assert body_dict["enableAI"] is True
    assert body_dict["enableAutoCorrection"] is False


def test_email_batch_analyze_json_with_name():
    wrapper, dummy = _prepare_email_wrapper()
    res = wrapper.batch_analyze({
        "emails": ["a@ex.com", "b@ex.com"],
        "enableAi": True,
        "enableAutoCorrection": True,
        "name": "my list",
    })
    assert res == {"batch": True}
    assert dummy.last_batch_body is not None
    body = dummy.last_batch_body.to_dict()
    assert set(body.keys()) >= {"emails", "enableAI", "enableAutoCorrection", "name"}
    assert body["name"] == "my list"
    assert body["enableAI"] is True
    assert body["enableAutoCorrection"] is True
    assert body["emails"] == ["a@ex.com", "b@ex.com"]


def test_email_batch_analyze_text_plain_requires_input():
    wrapper, _ = _prepare_email_wrapper()
    with pytest.raises(ValueError):
        wrapper.batch_analyze({}, content_type="text/plain")  # neither text nor emails


def test_email_batch_analyze_file_invalid_path():
    wrapper, _ = _prepare_email_wrapper()
    with pytest.raises(ValueError):
        wrapper.batch_analyze_file("/non/existent/nowhere.csv")


# --------------------- IpInsights tests ------------------------

def _prepare_ip_wrapper() -> tuple[IpInsights, _DummyIpApi]:
    wrapper = IpInsights("dummy-key")
    dummy = _DummyIpApi()
    wrapper.api_instance = dummy  # type: ignore[attr-defined]
    if hasattr(wrapper, "_config_changed"):
        wrapper._config_changed = False  # type: ignore[attr-defined]
    return wrapper, dummy


def test_ip_analyze_normalization():
    wrapper, dummy = _prepare_ip_wrapper()
    res = wrapper.analyze({"ip": "1.2.3.4", "enableAi": True})
    assert res == {"analyzeIp": True}
    assert dummy.last_analyze_body is not None
    body_dict = dummy.last_analyze_body.to_dict()
    assert body_dict["ip"] == "1.2.3.4"
    assert body_dict["enableAI"] is True


def test_ip_batch_analyze_with_name():
    wrapper, dummy = _prepare_ip_wrapper()
    res = wrapper.batch_analyze({"ips": ["1.1.1.1", "8.8.8.8"], "enableAi": False, "name": "prod-ips"})
    assert res == {"batchIp": True}
    assert dummy.last_batch_body is not None
    body = dummy.last_batch_body.to_dict()
    assert body["ips"] == ["1.1.1.1", "8.8.8.8"]
    assert body["name"] == "prod-ips"
    assert body.get("enableAI") is False


def test_ip_batch_requires_ips():
    wrapper, _ = _prepare_ip_wrapper()
    with pytest.raises(ValueError):
        wrapper.batch_analyze({})


# Additions for IpInsights extended batch support

def test_ip_batch_text_plain_build_from_list():
    # For text/plain path we need the real generated api_instance with an api_client
    wrapper = IpInsights("dummy-key")  # do not swap in dummy
    # Monkeypatch ApiClient.call_api to avoid network
    original_call = wrapper.api_instance.api_client.call_api  # type: ignore[attr-defined]

    class _Resp:
        def __init__(self):
            self.status = 202
            self.data = b'{"jobId":"abc123"}'
            self.headers = {}
            self.reason = "ACCEPTED"
        def read(self):
            return self.data
        def getheader(self, name, default=None):
            return None
        def getheaders(self):
            return {}

    def fake_call(method, url, headers=None, body=None, post_params=None, _request_timeout=None):  # noqa: D401
        return _Resp()

    wrapper.api_instance.api_client.call_api = fake_call  # type: ignore[attr-defined]
    try:
        res = wrapper.batch_analyze({"ips": ["1.2.3.4", "5.6.7.8"], "name": "list-to-text"}, content_type="text/plain")
        assert res["jobId"] == "abc123"
    finally:
        wrapper.api_instance.api_client.call_api = original_call  # type: ignore[attr-defined]


def test_ip_batch_text_plain_missing_inputs():
    wrapper, _ = _prepare_ip_wrapper()
    with pytest.raises(ValueError):
        wrapper.batch_analyze({}, content_type="text/plain")
