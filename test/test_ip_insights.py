# coding: utf-8

# Re-export the full wrapper test suite under the canonical name expected by assess_tests.py.
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from test_ip_insights_wrapper import TestIpInsightsWrapper  # noqa: F401

if __name__ == "__main__":
    import unittest
    unittest.main()
