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

## Single Analysis

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

## Batch Analysis

For processing large volumes of emails or IP addresses, use the batch analysis methods:

### Batch Email Analysis

```python
from opportify_sdk import EmailInsights

# Initialize the wrapper with your API key
api_key = "<YOUR-API-KEY-HERE>"
email_insights = EmailInsights(api_key)

# Define batch request parameters
batch_params = {
    "emails": [
        "user1@company.com",
        "user2@domain.org",
        "test@example.com"
    ],
    "enableAutoCorrection": True,
    "enableAi": True,
    "name": "my batch job 1"
}

# Start batch analysis
try:
    batch_response = email_insights.batch_analyze(batch_params)
    job_id = batch_response['job_id']
    print(f"Batch job started: {job_id}")
    
    # Check batch status
    status = email_insights.get_batch_status(job_id)
    print(f"Status: {status['status']}, Progress: {status['progress']}%")
    
    # When completed, download URLs will be available
    if status['status'] == 'COMPLETED':
        download_urls = status['download_urls']
        print(f"Results ready: {download_urls['csv']}")
        
except Exception as e:
    print(f"Error: {e}")
```

### Batch Email Analysis (File Upload Examples)

You can submit a large list of emails via a local CSV or plain text file. The CSV may contain one or multiple columns; the backend extracts all valid emails it finds. A plain text file should contain one email per line.

#### 1. Using the convenience helper `batch_analyze_file`

```python
from opportify_sdk import EmailInsights

api_key = "<YOUR-API-KEY-HERE>"
email_insights = EmailInsights(api_key)

try:
    response = email_insights.batch_analyze_file(
        "/path/to/emails.csv",
        enableAi=True,
        enableAutoCorrection=True,
        name="marketing-upload-oct"
    )
    print("Batch file upload started:", response)
    # Typical keys (camelCase) include: response['jobId']
except Exception as e:
    print(f"Error: {e}")
```

#### 2. Using the generic `batch_analyze` with explicit multipart content type

```python
from opportify_sdk import EmailInsights

api_key = "<YOUR-API-KEY-HERE>"
email_insights = EmailInsights(api_key)

params = {
    "file": "/path/to/emails.txt",  # Can also be .csv
    "enableAi": True,
    "enableAutoCorrection": False,
    "name": "text-upload-list"
}

try:
    response = email_insights.batch_analyze(params, content_type="multipart/form-data")
    print("Multipart batch started:", response)
except Exception as e:
    print(f"Error: {e}")
```

Notes:
* Use `enableAi` / `enableAutoCorrection` (camelCase) or their snake_case variants; both are accepted.
* The helper `batch_analyze_file` automatically sets the correct content type.
* The response uses camelCase keys (e.g., `jobId`, `downloadUrls`).

### Batch IP Analysis

```python
from opportify_sdk import IpInsights

# Initialize the wrapper with your API key
api_key = "<YOUR-API-KEY-HERE>"
ip_insights = IpInsights(api_key)

# Define batch request parameters
batch_params = {
    "ips": [
        "8.8.8.8",
        "1.1.1.1",
        "192.168.1.1"
    ],
    "enableAi": True,
    "name": "my batch job 1"
}

# Start batch analysis
try:
    batch_response = ip_insights.batch_analyze(batch_params)
    job_id = batch_response['job_id']
    print(f"Batch job started: {job_id}")
    
    # Check batch status
    status = ip_insights.get_batch_status(job_id)
    print(f"Status: {status['status']}, Progress: {status['progress']}%")
    
    # When completed, download URLs will be available
    if status['status'] == 'COMPLETED':
        download_urls = status['download_urls']
        print(f"Results ready: {download_urls['csv']}")
        
except Exception as e:
    print(f"Error: {e}")
```

### Batch IP Analysis (File Upload)

```python
from opportify_sdk import IpInsights

api_key = "<YOUR-API-KEY-HERE>"
ip_insights = IpInsights(api_key)

try:
    response = ip_insights.batch_analyze_file(
        "/path/to/ips.txt",  # one IP per line or CSV of IPs
        enableAi=True,
        name="edge-nodes-seed"
    )
    print("IP batch file job:", response['jobId'])
except Exception as e:
    print(f"Error: {e}")
```

### Batch IP Analysis (text/plain)

```python
from opportify_sdk import IpInsights

api_key = "<YOUR-API-KEY-HERE>"
ip_insights = IpInsights(api_key)

# Raw text submission
plain_response = ip_insights.batch_analyze(
    {"text": "1.1.1.1\n8.8.8.8", "name": "dns-providers"},
    content_type="text/plain"
)
print("Job:", plain_response['jobId'])

# Derived from list automatically
plain_response2 = ip_insights.batch_analyze(
    {"ips": ["10.0.0.1", "10.0.0.2"], "name": "internal-segment"},
    content_type="text/plain"
)
```

## Configuration

### Enable Debug Mode

```python
ip_insights.set_version("v1").set_debug_mode(True)
email_insights.set_version("v1").set_debug_mode(True)
```

### Batch Status Polling

For long-running batch jobs, poll the status periodically:

```python
import time

def wait_for_batch_completion(client, job_id, max_wait=300):
    """Wait for batch job to complete with polling."""
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status = client.get_batch_status(job_id)
        
        if status['status'] == 'COMPLETED':
            return status
        elif status['status'] == 'ERROR':
            raise Exception(f"Batch job failed: {status.get('status_description')}")
        
        print(f"Progress: {status.get('progress', 0)}%")
        time.sleep(10)  # Wait 10 seconds before next check
    
    raise TimeoutError("Batch job did not complete within the timeout period")

# Usage
try:
    batch_response = email_insights.batch_analyze(batch_params)
    final_status = wait_for_batch_completion(email_insights, batch_response['job_id'])
    print("Batch completed successfully!")
except Exception as e:
    print(f"Error: {e}")
```

## About this package

This Python package supports both single and batch analysis operations and is a customization of the base generated by:

- [OpenAPI Generator](https://openapi-generator.tech) project.

## Additional Resources

- **[Batch Processing Guide](BATCH_PROCESSING_GUIDE.md)** - Comprehensive guide for batch operations
- **[API Documentation](https://api.opportify.ai/docs)** - Full API reference
- **[Support](https://www.opportify.ai/support)** - Get help and support

