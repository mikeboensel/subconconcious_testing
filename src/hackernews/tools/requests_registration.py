def get_requests_tool(ngrok_url: str) -> dict:
    return {
        "type": "function",
        "name": "http_request",
        "description": "Make HTTP requests using the Python requests library. Supports GET, POST, PUT, DELETE, PATCH, HEAD, and OPTIONS methods with full control over headers, parameters, body data, and request options.",
        "url": ngrok_url,
        "method": "POST",
        "timeout": 30,
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to make the request to",
                },
                "method": {
                    "type": "string",
                    "enum": [
                        "GET",
                        "POST",
                        "PUT",
                        "DELETE",
                        "PATCH",
                        "HEAD",
                        "OPTIONS",
                    ],
                    "description": "HTTP method to use",
                    "default": "GET",
                },
                "headers": {
                    "type": "object",
                    "description": "HTTP headers to include in the request",
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters to append to the URL",
                },
                "data": {
                    "type": "string",
                    "description": "Request body data (for form data or raw body)",
                },
                "json": {
                    "type": "object",
                    "description": "JSON object to send as request body",
                },
                "timeout": {
                    "type": "number",
                    "description": "Request timeout in seconds",
                    "default": 30,
                },
                "allow_redirects": {
                    "type": "boolean",
                    "description": "Whether to follow redirects",
                    "default": True,
                },
                "verify": {
                    "type": "boolean",
                    "description": "Whether to verify SSL certificates",
                    "default": True,
                },
            },
            "required": ["url"],
        },
    }
