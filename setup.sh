#!/bin/bash

echo "🚀 Setting up the Flask API Gateway structure..."

# Step 1: Create a virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Step 2: Activate the virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Step 4: Install required dependencies
echo "📥 Installing dependencies..."
pip install flask requests gunicorn python-dotenv

# Step 5: Create the necessary project structure
echo "📂 Setting up directory structure..."
mkdir -p api_gateway
cd api_gateway

# Step 6: Create required files if they don’t exist
echo "📄 Creating necessary files..."

# Create main files
touch app.py config.py routes.py middleware.py services.py logger.py error_codes.py api_config.py .env

# Populate .env file with default values
echo "AUTH_SERVICE_URL=http://localhost:5001" > .env
echo "USER_SERVICE_URL=http://localhost:5002" >> .env

# Populate error_codes.py
cat <<EOL > error_codes.py
ERROR_CODES = {
    "token_expired": {"status": 401, "error_message": "Token is expired", "error_code": "TOKEN_EXPIRED"},
    "unauthorized": {"status": 401, "error_message": "Unauthorized access", "error_code": "UNAUTHORIZED"},
    "invalid_token": {"status": 401, "error_message": "Invalid token", "error_code": "INVALID_TOKEN"},
    "service_unavailable": {"status": 503, "error_message": "Service unavailable", "error_code": "SERVICE_UNAVAILABLE"},
    "invalid_endpoint": {"status": 404, "error_message": "Invalid endpoint", "error_code": "INVALID_ENDPOINT"}
}
EOL

# Populate api_config.py
cat <<EOL > api_config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5002")

API_CONFIG = {
    "auth_register": {"url": f"{AUTH_SERVICE_URL}/auth/register", "method": "POST", "auth_required": False},
    "auth_verify": {"url": f"{AUTH_SERVICE_URL}/auth/verify", "method": "POST", "auth_required": False},
    "auth_refresh": {"url": f"{AUTH_SERVICE_URL}/auth/refresh", "method": "POST", "auth_required": False},
    "user_profile": {"url": f"{USER_SERVICE_URL}/user/profile", "method": "GET", "auth_required": True}
}
EOL

# Step 7: Generate a requirements.txt file
echo "📌 Saving dependencies..."
pip freeze > requirements.txt

echo "✅ Flask API Gateway structure is set up!"
echo "To start working, activate your virtual environment using:"
echo "source venv/bin/activate"
