# coding: utf-8

"""
Unit tests for FraudProtection wrapper class.

Tests cover:
- Configuration management (host, prefix, version, debug mode, method chaining)
- analyze_fraud() success
- analyze_fraud() ApiException handling
- Parameter normalization (snake_case + camelCase aliases, required field validation)
"""

import unittest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from opportify_sdk import FraudProtection
from fraud_intel_client.exceptions import ApiException


class TestFraudProtectionWrapper(unittest.TestCase):
    """FraudProtection wrapper unit tests"""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.api_key = "test-api-key-123"
        self.mock_api = Mock()
        self.fraud_protection = FraudProtection(self.api_key, api_instance=self.mock_api)

    # ========== Configuration Tests ==========

    def test_initialization(self) -> None:
        """Test FraudProtection initialization with default values."""
        client = FraudProtection("test-key")
        self.assertEqual(client.host, "https://api.opportify.ai")
        self.assertEqual(client.prefix, "intel")
        self.assertEqual(client.version, "v1")
        self.assertEqual(client.debug_mode, False)
        self.assertEqual(client.final_url, "https://api.opportify.ai/intel/v1")

    def test_set_host(self) -> None:
        """Test setting custom host."""
        self.fraud_protection.set_host("https://api.staging.opportify.ai")
        self.assertEqual(self.fraud_protection.host, "https://api.staging.opportify.ai")
        self.assertTrue(self.fraud_protection.config_changed)

    def test_set_version(self) -> None:
        """Test setting custom API version."""
        self.fraud_protection.set_version("v2")
        self.assertEqual(self.fraud_protection.version, "v2")
        self.assertTrue(self.fraud_protection.config_changed)

    def test_set_prefix(self) -> None:
        """Test setting custom URL prefix."""
        self.fraud_protection.set_prefix("custom")
        self.assertEqual(self.fraud_protection.prefix, "custom")
        self.assertTrue(self.fraud_protection.config_changed)

    def test_set_prefix_strips_slashes(self) -> None:
        """Test that set_prefix strips leading/trailing slashes."""
        self.fraud_protection.set_prefix("/intel/")
        self.assertEqual(self.fraud_protection.prefix, "intel")

    def test_set_debug_mode(self) -> None:
        """Test enabling debug mode."""
        self.fraud_protection.set_debug_mode(True)
        self.assertTrue(self.fraud_protection.debug_mode)
        self.assertTrue(self.fraud_protection.config_changed)

    def test_method_chaining(self) -> None:
        """Test that setter methods support chaining."""
        result = (self.fraud_protection
                  .set_host("https://custom.api.com")
                  .set_version("v2")
                  .set_prefix("custom")
                  .set_debug_mode(True))
        self.assertIs(result, self.fraud_protection)

    def test_update_final_url(self) -> None:
        """Test final URL construction."""
        self.fraud_protection.host = "https://api.example.com"
        self.fraud_protection.prefix = "intel"
        self.fraud_protection.version = "v1"
        self.fraud_protection._update_final_url()
        self.assertEqual(self.fraud_protection.final_url, "https://api.example.com/intel/v1")

    def test_update_final_url_no_prefix(self) -> None:
        """Test final URL construction without prefix."""
        self.fraud_protection.host = "https://api.example.com"
        self.fraud_protection.prefix = ""
        self.fraud_protection.version = "v1"
        self.fraud_protection._update_final_url()
        self.assertEqual(self.fraud_protection.final_url, "https://api.example.com/v1")

    def test_update_final_url_no_version(self) -> None:
        """Test final URL construction without version."""
        self.fraud_protection.host = "https://api.example.com"
        self.fraud_protection.prefix = "intel"
        self.fraud_protection.version = ""
        self.fraud_protection._update_final_url()
        self.assertEqual(self.fraud_protection.final_url, "https://api.example.com/intel")

    # ========== analyze_fraud Tests ==========

    def test_analyze_fraud_success_with_email(self) -> None:
        """Test successful fraud analysis with email."""
        mock_response = Mock()
        mock_response.to_dict.return_value = {"riskScore": 25, "riskLevel": "low"}
        self.mock_api.analyze_fraud.return_value = mock_response

        params = {"email": "user@example.com", "origin": "example.com"}
        result = self.fraud_protection.analyze_fraud(params)

        self.assertEqual(result["riskScore"], 25)
        self.mock_api.analyze_fraud.assert_called_once()

    def test_analyze_fraud_success_with_user_ip(self) -> None:
        """Test successful fraud analysis with userIp only."""
        mock_response = Mock()
        mock_response.to_dict.return_value = {"riskScore": 10, "riskLevel": "low"}
        self.mock_api.analyze_fraud.return_value = mock_response

        params = {"userIp": "1.2.3.4"}
        result = self.fraud_protection.analyze_fraud(params)

        self.assertEqual(result["riskScore"], 10)
        self.mock_api.analyze_fraud.assert_called_once()

    def test_analyze_fraud_success_with_snake_case_user_ip(self) -> None:
        """Test that snake_case user_ip alias is accepted."""
        mock_response = Mock()
        mock_response.to_dict.return_value = {"riskScore": 10}
        self.mock_api.analyze_fraud.return_value = mock_response

        params = {"user_ip": "1.2.3.4"}
        result = self.fraud_protection.analyze_fraud(params)

        self.assertEqual(result["riskScore"], 10)

    def test_analyze_fraud_success_with_full_payload(self) -> None:
        """Test fraud analysis with all optional fields."""
        mock_response = Mock()
        mock_response.to_dict.return_value = {"riskScore": 50, "riskLevel": "medium"}
        self.mock_api.analyze_fraud.return_value = mock_response

        params = {
            "email": "user@example.com",
            "userIp": "1.2.3.4",
            "firstName": "John",
            "lastName": "Doe",
            "companyName": "Acme Corp",
            "origin": "example.com",
            "submissionType": "registration",
            "formData": {"custom_field": "value"},
        }
        result = self.fraud_protection.analyze_fraud(params)

        self.assertEqual(result["riskLevel"], "medium")
        self.mock_api.analyze_fraud.assert_called_once()

    def test_analyze_fraud_camel_and_snake_aliases(self) -> None:
        """Test that both camelCase and snake_case aliases map to the same normalized field."""
        mock_response = Mock()
        mock_response.to_dict.return_value = {"riskScore": 0}
        self.mock_api.analyze_fraud.return_value = mock_response

        for params in [
            {"email": "a@b.com", "firstName": "Jane"},
            {"email": "a@b.com", "first_name": "Jane"},
        ]:
            self.fraud_protection.analyze_fraud(params)

        self.assertEqual(self.mock_api.analyze_fraud.call_count, 2)

    def test_analyze_fraud_missing_required_fields(self) -> None:
        """Test that omitting both email and userIp raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.fraud_protection.analyze_fraud({"firstName": "John"})
        self.assertIn("email", str(ctx.exception).lower())

    def test_analyze_fraud_api_exception_403(self) -> None:
        """Test analyze_fraud handles 403 Forbidden."""
        self.mock_api.analyze_fraud.side_effect = ApiException(status=403, reason="Forbidden")

        with self.assertRaises(Exception) as ctx:
            self.fraud_protection.analyze_fraud({"email": "user@example.com"})
        self.assertIn("API exception", str(ctx.exception))

    def test_analyze_fraud_api_exception_500(self) -> None:
        """Test analyze_fraud handles 500 Internal Server Error."""
        self.mock_api.analyze_fraud.side_effect = ApiException(
            status=500, reason="Internal Server Error"
        )

        with self.assertRaises(Exception) as ctx:
            self.fraud_protection.analyze_fraud({"email": "user@example.com"})
        self.assertIn("API exception", str(ctx.exception))

    def test_analyze_fraud_api_exception_402(self) -> None:
        """Test analyze_fraud handles 402 Payment Required."""
        self.mock_api.analyze_fraud.side_effect = ApiException(
            status=402, reason="Payment Required"
        )

        with self.assertRaises(Exception) as ctx:
            self.fraud_protection.analyze_fraud({"email": "user@example.com"})
        self.assertIn("API exception", str(ctx.exception))

    def test_analyze_fraud_api_exception_429(self) -> None:
        """Test analyze_fraud handles 429 Too Many Requests."""
        self.mock_api.analyze_fraud.side_effect = ApiException(
            status=429, reason="Too Many Requests"
        )

        with self.assertRaises(Exception) as ctx:
            self.fraud_protection.analyze_fraud({"email": "user@example.com"})
        self.assertIn("API exception", str(ctx.exception))

    # ========== Normalization Tests ==========

    def test_normalize_form_data_must_be_dict(self) -> None:
        """Test that non-dict formData raises ValueError."""
        with self.assertRaises(ValueError):
            self.fraud_protection._normalize_request(
                {"email": "a@b.com", "form_data": "not-a-dict"}
            )

    def test_normalize_form_data_camel_alias(self) -> None:
        """Test that camelCase formData alias is accepted."""
        normalized = self.fraud_protection._normalize_request(
            {"email": "a@b.com", "formData": {"key": "val"}}
        )
        self.assertEqual(normalized["form_data"], {"key": "val"})

    def test_normalize_omits_none_optional_fields(self) -> None:
        """Test that optional fields not supplied are absent from normalized output."""
        normalized = self.fraud_protection._normalize_request({"email": "a@b.com"})
        self.assertNotIn("phone1", normalized)
        self.assertNotIn("first_name", normalized)
        self.assertNotIn("form_data", normalized)


if __name__ == "__main__":
    unittest.main()
