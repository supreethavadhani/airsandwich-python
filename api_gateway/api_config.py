import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://0.0.0.0:5001")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5002")

API_CONFIG = {
    "auth_register": {"url": f"{AUTH_SERVICE_URL}/auth/register", "method": "POST", "auth_required": False},
    "auth_verify": {"url": f"{AUTH_SERVICE_URL}/auth/verify", "method": "POST", "auth_required": False},
    "auth_refresh": {"url": f"{AUTH_SERVICE_URL}/auth/refresh", "method": "POST", "auth_required": False},
    "user_profile": {"url": f"{USER_SERVICE_URL}/user/profile", "method": "GET", "auth_required": True}
}
