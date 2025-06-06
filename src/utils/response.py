"""
HTTP response utilities for Lambda functions.

This module provides standardized response formatting for API Gateway
Lambda functions with proper CORS headers and consistent structure.
"""

import json
from typing import Any, Dict, Optional


def create_response(
    status_code: int, body: Dict[str, Any], headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Create a standardized API Gateway response.

    Args:
        status_code: HTTP status code
        body: Response body data
        headers: Optional additional headers

    Returns:
        Formatted API Gateway response dictionary
    """
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
    }

    if headers:
        default_headers.update(headers)

    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body),
    }


def success_response(data: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
    """Create a successful response (200)."""
    return create_response(200, {"message": message, "data": data})


def error_response(error: str, status_code: int = 400) -> Dict[str, Any]:
    """Create an error response."""
    return create_response(status_code, {"error": error})


def validation_error_response(errors: Any) -> Dict[str, Any]:
    """Create a validation error response (400)."""
    return create_response(400, {"error": "Validation failed", "details": errors})
