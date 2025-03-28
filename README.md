# Opportify-SDK-Python

## Overview

The **Opportify Insights API** provides access to a powerful and up-to-date platform. With advanced data warehousing and AI-driven capabilities, this API is designed to empower your business to make informed, data-driven decisions and effectively assess potential risks.

[Sign Up Free](https://www.opportify.ai)

### Base URL
Use the following base URL for all API requests:

```plaintext
https://api.opportify.ai/insights/v1/<service>/<endpoint>
```

## Requirements

Requires Python v3.8 or later

## Getting Started

First, install Opportify SDK via PyPI manager:

```
pip install opportify-sdk
```

### Calling Email Insights

```python
from opportify_sdk import EmailInsights

# Initialize the wrapper with your API key
api_key = "<YOUR-API-KEY-HERE>"
email_insights = EmailInsights(api_key)

# Optional: Configure host, version, and debug mode
email_insights.set_version("v1")

# Define request parameters
params = {
    "email": "<SOME-EMAIL-HERE>",
    "enableAutoCorrection": True,
    "enableAi": True 
}

# Call the API
try:
    result = email_insights.analyze(params)
    print("Response:", result)
except Exception as e:
    print(f"Error: {e}")
```

### Calling IP Insights

```python

from opportify_sdk import IpInsights

# Initialize the wrapper with your API key
api_key = "<YOUR-API-KEY-HERE>"
ip_insights = IpInsights(api_key)

# Optional: Configure host, version, and debug mode
ip_insights.set_version("v1")

# Define request parameters
params = {
    "ip": "<SOME-IP-HERE>",
    "enableAi": True 
}

# Call the API
try:
    result = ip_insights.analyze(params)
    print("Response:", result)
except Exception as e:
    print(f"Error: {e}")
```

### Enable Debug Mode

```python
ip_insights.set_version("v1").set_debug_mode(True)
email_insights.set_version("v1").set_debug_mode(True)
```

## About this package

This Python package is a customization of the base generated by:

- [OpenAPI Generator](https://openapi-generator.tech) project.

