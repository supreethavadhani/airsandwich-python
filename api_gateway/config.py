import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Global configuration settings for the Flask API Gateway."""

    # Flask Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # Service URLs (Loaded from .env)
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5002")

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # Request Timeouts
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 5))  # Default: 5 seconds

    # Rate Limits (If needed)
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/min")  # Example format

# Create an instance to use across the app
config = Config()
