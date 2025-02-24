from flask import Blueprint
from utils import require_token, forward_request

# Create Blueprint for User Service
user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"], endpoint="user_profile")
@require_token
def user_profile():
    return forward_request("user_profile")
