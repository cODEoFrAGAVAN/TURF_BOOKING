from .models import *
import secrets
import base64


def authenticate_user(user_name, password):
    try:
        user = Turf_registration.objects.filter(user_name=user_name, password=password)
        # Check if the provided password matches the stored password
        if user:
            return True  # Authentication successful
        else:
            return False  # Authentication failed
    except Turf_registration.DoesNotExist:
        return False


def user_secret_key():
    # Generate a secure 32-byte (256-bit) key
    secure_key = secrets.token_bytes(32)

    # Optionally encode it in base64 for easier storage or transmission
    secure_key_base64 = base64.urlsafe_b64encode(secure_key).decode("utf-8")
    return secure_key_base64
