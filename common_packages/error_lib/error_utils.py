from flask import jsonify
from typing import Literal
from error_lib.error_codes import ERROR_CODES

# Define allowed error keys for better autocomplete support
ErrorKeys = Literal[
    "token_expired",
    "unauthorized",
    "invalid_token",
    "service_unavailable",
    "invalid_endpoint"
]

def get_error_response(error_key: ErrorKeys):
    """
    Returns a standardized JSON error response.

    Args:
        error_key (Literal): The key corresponding to the error in ERROR_CODES.

    Returns:
        Flask Response: JSON response with error message and status code.

    Example:
        >>> get_error_response("invalid_token")
        {
            "error": "Invalid token",
            "error_code": "INVALID_TOKEN"
        }
    """
    error_data = ERROR_CODES.get(error_key, ERROR_CODES["invalid_endpoint"])
    return jsonify({"error": error_data["error_message"], "error_code": error_data["error_code"]}), error_data["status"]
