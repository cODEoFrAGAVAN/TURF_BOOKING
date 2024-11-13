from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import JsonResponse
import jwt
import random
import pandas as pd
from datetime import datetime, timedelta
import time
import logging, traceback
from .auth import *
from rest_framework import status
import logging


logger = logging.getLogger(__name__)


@api_view(["POST"])
def login(request):
    try:
        serializer = Login_serializer1(data=request.data)
        if serializer.is_valid():
            auth = authenticate_user(
                user_name=request.data["user_name"], password=request.data["password"]
            )
            if auth:
                expired_time = (datetime.now() + timedelta(days=1)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                user = User_signup.objects.get(user_name=request.data["user_name"])
                secret_key = Random_token_generation.objects.get(
                    user_name=request.data["user_name"]
                )
                payload = {
                    "date": user.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "user_name": user.user_name,
                    "password": user.password,
                    "exp_time": expired_time,
                }
                # print(secret_key.random_token)
                # print(payload)
                encoded = jwt.encode(
                    payload, (secret_key.random_token), algorithm="HS256"
                )
                return Response(
                    {"msg": "Log in successfully", "stat": "Ok", "token": encoded},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response({"msg": "Log in failed", "stat": "Ok"}, status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {
                    "msg": "Log in failed",
                    "stat": "Not Ok",
                    "error": serializer.error_messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        # logger.error('An error occured %s'+traceback.format_exc())
        logger.error("login error :: " + str(e) + " :: traceback :: " + traceback.format_exc())
        return Response(
            {
                "error": str(e),
                "stat": "Not Ok",
                "traceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def user_signin_up(request):
    try:
        input_data = request.data.copy()
        token_dict = dict(time)
        input_data["created_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = User_Signup_serializer1(data=input_data)
        if serializer.is_valid():
            serializer.save()
            token_dict["user_name"] = input_data["user_name"]
            token_dict["mobile"] = input_data["mobile_number"]
            token_dict["random_token"] = str(user_secret_key())
            serializer1 = Random_token_seriallizer1(data=token_dict)
            if serializer1.is_valid():
                serializer1.save()
                return Response(
                    {
                        "stat": "Ok",
                        "msg": "User created",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "stat": "Not Ok",
                        "msg": "User not created",
                        "error": serializer1.errors,
                    },
                    status = status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {
                    "stat": "Not Ok",
                    "msg": "User not created",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        logger.error(
            " :: user_signin_up :: "
            + str(e)
            + " :: traceback :: "
            + traceback.format_exc()
        )
        return Response(
            {
                "error": str(e),
                "traceback": str(traceback.format_exc()),
                "stat": "Not Ok",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
@api_view(['POST'])
def forget_user_password(request):
    try:
        input_data = request.data.copy()
        user_name = input_data.get("user_name",None)
        random_number = random.randint(100000, 999999)
        user = User_signup.objects.get(user_name=user_name)
        # print("user : : ",user)
        input_data['mobile_number'] = user.mobile_number
        input_data['mailid'] = user.mailid
        input_data['otp'] = str(random_number)
        serializer = Forget_user_password_serializer1(data = input_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "stat":"Ok",
                "otp":str(random_number),
                "msg":"otp sent to your registered mail id and mobile number"
            },status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "stat":"Not Ok",
                    "error":serializer.errors,
                    "msg":"otp not sent"
                },status=status.HTTP_401_UNAUTHORIZED
            )
    except User_signup.DoesNotExist:
        return Response(
            {
                'stat':'Not Ok',
                'error':"user doesn't exists"
            },status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        logger.error(": : forget password error : : "+str(e)+" : : traceback : : "+traceback.format_exc())
        return Response({
            "stat":"Not Ok",
            "error":str(e),
            "traceback":str(traceback.format_exc())
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
def verify_otp(request):
    try:
        input_data = request.data.copy()
        user_name = input_data.get("input_data",None)
        otp = input_data.get("otp",None)
        if user_name is None or otp is None:
            return Response(
                {
                    'stat':'Not Ok',
                    'error':'give correct credentials'
                },status=status.HTTP_401_UNAUTHORIZED
            )
        saved_otp = Forget_user_password.objects.get(user_name = input_data['user_name'],otp = input_data['otp'])
        if saved_otp.user_name == user_name and saved_otp.otp == otp:
            return Response(
                {
                    "stat":"Ok",
                    "msg":"otp matched"
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "stat":"Not Ok",
                    "msg":"otp not mathced with this user name"
                },status=status.HTTP_401_UNAUTHORIZED
            )
    except Forget_user_password.DoesNotExist:
        return Response(
                {
                    "stat":"Not Ok",
                    "msg":"otp not mathced with this user name"
                },status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        logger.error(": : verify otp error : : "+str(e)+" : :  traceback : : "+traceback.format_exc())
        return Response(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def update_password(request):
    try:
        input_data = request.data.copy()
        saved_otp = Forget_user_password.objects.get(user_name = input_data['user_name'],otp = input_data['otp'],isvalid = 'True')
        saved_otp.isvalid = 'False'
        saved_otp.save()
        update_pass = User_signup.objects.get(user_name=request.data["user_name"])
        update_pass.password = input_data['new_password']
        update_pass.save()
        return Response(
            {
                "stat":"Ok",
                "msg":"Password updated successfully"
            },status.HTTP_200_OK
        )
    except Forget_user_password.DoesNotExist:
        return Response(
            {
                "stat":"Not Ok",
                "msg":"otp not mathced with this user name"
            },status=status.HTTP_401_UNAUTHORIZED
        )
    except update_pass.DoesNotExist:
        return Response(
            {
                "stat":"Not Ok",
                "msg":"user doesn't exists"
            },status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        logger.error(": : update password error : : "+str(e)+" : :  traceback : : "+traceback.format_exc())
        return Response(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
