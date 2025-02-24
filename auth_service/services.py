from models import db, User
from jwt_utils import generate_tokens, decode_token
from common_packages.error_lib.error_utils import get_error_response  # ✅ Standardized error handling
import logging

# Logger setup
logger = logging.getLogger(__name__)

def generate_otp(email):
    """
    Generates a new OTP, stores it in the user record, and returns the OTP.
    """
    try:
        user = User.query.filter_by(email=email).first()
        
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        otp = user.generate_otp()  # Call the generate_otp() method
        db.session.commit()

        return otp  # Return OTP for now (should be sent via email)

    except Exception as e:
        logger.error(f"Error generating OTP for {email}: {e}")
        return None

def verify_otp(email, otp_code):
    """
    Verifies the OTP and generates JWT tokens if valid.
    """
    try:
        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_otp(otp_code):
            return False, get_error_response("invalid_token")  # ✅ Use standardized error

        user.is_otp_verified = True
        user.encrypted_otp = None  # Clear OTP after verification
        user.otp_salt = None
        user.otp_expiry = None
        db.session.commit()

        return True, generate_tokens(user.id)

    except Exception as e:
        logger.error(f"Error verifying OTP for {email}: {e}")
        return False, get_error_response("service_unavailable")  # ✅ Standardized error

async def refresh_access_token(refresh_token):
    """
    Refresh the access token using a valid refresh token.
    """
    print("entering refresh_access_token service---->")
    if not refresh_token:
        return False, get_error_response("unauthorized")  # ✅ Standardized error

    claims = await decode_token(refresh_token)

    logger.error(f"claims: {claims}")
    if "error" in claims:
        error_code = "REFRESH_TOKEN_EXPIRED" if claims["error"] == "TOKEN_EXPIRED" else "INVALID_REFRESH_TOKEN"
        return False, get_error_response(error_code)  # ✅ Standardized error

    # Extract user ID from the token
    user_id = claims.get("user_id")

    if not user_id:
        return False, get_error_response("invalid_token")  # ✅ Standardized error

    # Generate new access and refresh tokens
    new_tokens = generate_tokens(user_id)
    return True, new_tokens

def validate_token(access_token):
    """
    if token is expired throw a token_expired error.
    decode token and look for user id 
    if user doesnt exist throw invalid token error
    """
    #print to console
    print("entering validate_token service---->")
    if not access_token:
        return False, get_error_response("invalid_token")

    claims = decode_token(access_token)
    if "error" in claims:
        error_code = "REFRESH_TOKEN_EXPIRED" if claims["error"] == "TOKEN_EXPIRED" else "INVALID_REFRESH_TOKEN"
        return False, get_error_response(error_code) 
    
    user_id = claims.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return False, get_error_response("unauthorized")
    
    return True
    
