import requests
import logging
from functools import wraps
from flask import request, jsonify
from config import config
from common_packages.error_lib.error_utils import get_error_response  # ✅ Use centralized error handling
from api_config import API_CONFIG

# Initialize logger
logger = logging.getLogger(__name__)

def require_token(f):
    """
    Decorator to enforce authentication if required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        endpoint = request.endpoint
        config_entry = API_CONFIG.get(endpoint)
        print("helllooooo world")
        if config_entry and config_entry.get("auth_required", False):
            token = request.headers.get("x-access-token")

            if not token:
                logger.warning(f"Unauthorized access attempt to {endpoint}")
                return get_error_response("unauthorized")  # ✅ Standardized error

            try:
                auth_response = requests.get(
                    f"{config.AUTH_SERVICE_URL}/auth/validate",
                    headers={"Authorization": token}
                )
                print(auth_response.status_code)
                if auth_response.status_code != 200:
                    logger.warning(f"Invalid token for {endpoint}")
                    return get_error_response("invalid_token")  # ✅ Standardized error
            except requests.exceptions.RequestException as e:
                logger.error(f"Error connecting to auth service: {e}")
                return get_error_response("service_unavailable")  # ✅ Standardized error

        return f(*args, **kwargs)

    return decorated_function

def forward_request(endpoint):
    """
    Forward requests to respective microservices based on API_CONFIG.
    """
    config_entry = API_CONFIG.get(endpoint)

    if not config_entry:
        return get_error_response("invalid_endpoint")  # ✅ Standardized error

    try:
        response = requests.request(
            method=config_entry["method"],
            url=config_entry["url"],
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json() if request.method in ["POST", "PUT"] else None
        )
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        logger.error(f"Error forwarding request to {config_entry['url']}: {e}")
        return get_error_response("service_unavailable")  # ✅ Standardized error
