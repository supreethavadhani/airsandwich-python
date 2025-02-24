import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the Auth Service."""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root@mysql/air_sandwich_python")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secretkey")
    
    # Token Expiry Configurations
    OTP_EXPIRY = int(os.getenv("OTP_EXPIRY", 5))  # Default 5 minutes
    ACCESS_TOKEN_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY", 15))  # Default 15 minutes
    REFRESH_TOKEN_EXPIRY = int(os.getenv("REFRESH_TOKEN_EXPIRY", 30))  # Default 30 days

# Create a config instance
config = Config()
