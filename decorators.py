# decorators.py
from functools import wraps
import jwt
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging, traceback
from user.models import *
from datetime import *

logger = logging.getLogger(__name__)

def authorize(func):
    @wraps(func)
    def decorated_function(request, *args, **kwargs):
        authorization_header = request.META.get('HTTP_SEC')
        authorization_id = request.META.get('HTTP_ID')
        print("authorization_header",authorization_header,type(authorization_header))
        print("authorization_id",authorization_id,type(authorization_header))

        if authorization_header and authorization_id:
            secret_key = Random_token_generation.objects.get(
                    user_name=authorization_id
                )
            token = authorization_header
            print("secret_key.random_token :: ",secret_key.random_token)
            try:
                payload = jwt.decode(token, secret_key.random_token, algorithms=["HS256"])
                print(payload,":: payload ::")
                if authorization_id == payload.get('user_name') and datetime.strptime(payload.get('exp_time'),"%Y-%m-%d %H:%M:%S") >= datetime.now():
                    pass
                elif authorization_id != payload.get('user_name'):
                    return Response({"msg": "Token not matched."}, status=status.HTTP_401_UNAUTHORIZED)    
                elif datetime.strptime(payload.get('exp_time'),"%Y-%m-%d %H:%M:%S") < datetime.now():
                    return Response({"msg": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({"msg": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                return Response({"msg": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"msg": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                logger.error("Error in token validation: %s", traceback.format_exc())
                print("Error in token validation:", str(traceback.format_exc()))
                return Response({"msg": "Error occurred in token validation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return func(request, *args, **kwargs)
        else:
            return Response({"msg": "Authorization id and Authorization token required."}, status=status.HTTP_401_UNAUTHORIZED)

    return decorated_function
