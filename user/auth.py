from .models import *
import secrets
import base64
import logging

logger = logging.getLogger('django')


def authenticate_user(user_name, password):
    try:
        user = User_signup.objects.filter(user_name=user_name,password=password)
        # Check if the provided password matches the stored password
        if user:
            return True  # Authentication successful
        else:
            return False  # Authentication failed
    except User_signup.DoesNotExist:
        return False
    except Exception as e:
        logger.error("Error in authenticate user :: %s",e,exc_info=True)
        return False



def user_secret_key():
    try:
    # Generate a secure 32-byte (256-bit) key
        secure_key = secrets.token_bytes(32)

        # Optionally encode it in base64 for easier storage or transmission
        secure_key_base64 = base64.urlsafe_b64encode(secure_key).decode('utf-8')
        return secure_key_base64
    except Exception as e:
        logger.error("Error in user secret key generation :: %s",e,exc_info=True)
        return False


