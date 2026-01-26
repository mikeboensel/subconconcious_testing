from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, Literal
import requests

app = FastAPI(title="Requests Tool API")


class HttpRequest(BaseModel):
    """Request model for making HTTP requests using the requests library."""

    url: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"] = "GET"
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    data: Optional[Any] = None
    json: Optional[Dict[str, Any]] = None
    timeout: Optional[float] = 30.0
    allow_redirects: bool = True
    verify: bool = True


class HttpResponse(BaseModel):
    """Response model for HTTP requests."""

    status_code: int
    headers: Dict[str, str]
    text: Optional[str] = None
    json: Optional[Any] = None
    url: str
    elapsed: float  # Time elapsed in seconds


@app.post("/request", response_model=HttpResponse)
async def make_request(req: HttpRequest):
    """
    Make an HTTP request using the Python requests library.
    Supports all common HTTP methods and request options.
    """
    try:
        # Prepare request arguments
        request_kwargs = {
            "timeout": req.timeout,
            "allow_redirects": req.allow_redirects,
            "verify": req.verify,
        }

        if req.headers:
            request_kwargs["headers"] = req.headers
        if req.params:
            request_kwargs["params"] = req.params
        if req.data is not None:
            request_kwargs["data"] = req.data
        if req.json is not None:
            request_kwargs["json"] = req.json

        # Make the request
        response = requests.request(method=req.method, url=req.url, **request_kwargs)

        # Try to parse JSON, otherwise use text
        response_json = None
        response_text = None
        try:
            response_json = response.json()
        except (ValueError, requests.exceptions.JSONDecodeError):
            response_text = response.text

        return HttpResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            url=str(response.url),
            elapsed=response.elapsed.total_seconds(),
            json=response_json,
            text=response_text,
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408,
            detail=f"Request to {req.url} timed out after {req.timeout} seconds",
        )
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "library": "requests"}

    # Example usage (when running this as FastAPI app via uvicorn):
    # $ uvicorn tools.requests_tool:app --reload --port 8080
    #
    # Example cURL:
    # curl -X POST "http://localhost:8080/http_request" \
    #      -H "Content-Type: application/json" \
    #      -d '{"url": "https://httpbin.org/get", "method": "GET"}'
    #
    # Example response:
    # {
    #   "status_code": 200,
    #   "headers": { ... },
    #   "url": "https://httpbin.org/get",
    #   "elapsed": 0.178,
    #   "json": {
    #     "args": {},
    #     "headers": {...},
    #     ...
    #   },
    #   "text": null
    # }
