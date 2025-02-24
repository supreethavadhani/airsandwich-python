from flask import Blueprint, request, jsonify
from services import generate_otp, verify_otp, refresh_access_token, validate_token
from common_packages.error_lib.error_utils import get_error_response  # ✅ Import error handler

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a user and generate an OTP.
    """
    data = request.get_json()
    email = data.get("email")

    if not email:
        return get_error_response("unauthorized")  # ✅ Standardized error response

    otp = generate_otp(email)
    return jsonify({"message": "OTP sent", "otp": otp}), 200  # Remove OTP in production

@auth_bp.route("/verify", methods=["POST"])
def verify():
    """
    Verify the OTP and return access/refresh tokens if successful.
    """
    data = request.get_json()
    email = data.get("email")
    otp_code = data.get("otp")

    if not email or not otp_code:
        return get_error_response("invalid_token")  # ✅ Standardized error response

    success, result = verify_otp(email, otp_code)
    if not success:
        return get_error_response("invalid_token")  # ✅ Use predefined error

    return jsonify(result), 200

@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """
    Handles refresh token requests and provides a new access token.
    """
    refresh_token = request.headers.get("x-refresh-token")
    print("refresh_token",refresh_token)
    if not refresh_token:
        return get_error_response("unauthorized")  # ✅ Standardized error

    success, result = refresh_access_token(refresh_token)
    return (jsonify(result), 200) if success else get_error_response("token_expired")

@auth_bp.route("/validate", methods=["GET"])
def validate_token():
    """
    Validate the access token.
    """
    print("validate_token")
    access_token = request.headers.get("x-access-token")
    if not access_token:
        return get_error_response("unauthorized")
    #check if user exisits with user id
    success = validate_token(access_token)
    return (jsonify(success),200) if success else get_error_response("unauthorized")


