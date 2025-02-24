"""
Error Codes Library for Microservices.
Defines standardized error responses for the system.
"""

ERROR_CODES = {
    "token_expired": {"status": 401, "error_message": "Token is expired", "error_code": "TOKEN_EXPIRED"},
    "unauthorized": {"status": 401, "error_message": "Unauthorized access", "error_code": "UNAUTHORIZED"},
    "invalid_token": {"status": 401, "error_message": "Invalid token", "error_code": "INVALID_TOKEN"},
    "service_unavailable": {"status": 503, "error_message": "Service unavailable", "error_code": "SERVICE_UNAVAILABLE"},
    "invalid_endpoint": {"status": 404, "error_message": "Invalid endpoint", "error_code": "INVALID_ENDPOINT"}
}
