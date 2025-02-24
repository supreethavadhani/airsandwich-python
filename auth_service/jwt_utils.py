import jwt
import datetime
import logging
from config import config
from common_packages.error_lib.error_utils import get_error_response  # ✅ Standardized error handling

# Logger setup
logger = logging.getLogger(__name__)

def generate_tokens(user_id):
    """
    Generate JWT access and refresh tokens using values from config.

    Args:
        user_id (str): The unique user ID for whom the token is generated.

    Returns:
        dict: A dictionary containing "accessToken" and "refreshToken".
    """
    try:
        access_token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=config.ACCESS_TOKEN_EXPIRY),
            },
            config.JWT_SECRET_KEY,
            algorithm="HS256",
        )

        refresh_token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=config.REFRESH_TOKEN_EXPIRY),
            },
            config.JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return {"accessToken": access_token, "refreshToken": refresh_token}

    except Exception as e:
        logger.error(f"Error generating tokens for user {user_id}: {e}")
        return get_error_response("service_unavailable")  # ✅ Standardized error

def decode_token(token):
    """
    Decode a JWT token and return the payload.

    Args:
        token (str): The JWT token to be decoded.

    Returns:
        dict: The payload if successful, or an error response.
    """
    print(token)
    try:
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
    
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return get_error_response("token_expired")  # ✅ Standardized error
    
    except jwt.InvalidTokenError:
        logger.warning("Invalid token received")
        return get_error_response("invalid_token")  # ✅ Standardized error

    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return get_error_response("service_unavailable")  # ✅ Standardized error
