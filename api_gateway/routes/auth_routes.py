from flask import Blueprint
from utils import require_token, forward_request  # ✅ Absolute Import

# Create Blueprint for Auth Service
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"], endpoint="auth_register")
@require_token
def register():
    return forward_request("auth_register")

@auth_bp.route("/verify", methods=["POST"], endpoint="auth_verify")
@require_token
def verify_otp():
    return forward_request("auth_verify")

@auth_bp.route("/refresh", methods=["POST"], endpoint="auth_refresh")
@require_token
def refresh_token():
    print("refresh_token is called")
    return forward_request("auth_refresh")

