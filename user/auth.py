from .models import *

def authenticate_user(user_name, password):
    try:
        user = User_signup.object.get(user_name=user_name)
        # Check if the provided password matches the stored password
        if user.password == password:
            return True  # Authentication successful
        else:
            return False  # Authentication failed
    except User_signup.DoesNotExist:
        return False
