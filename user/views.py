from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import jwt
import random
import pandas as pd
from datetime import *
import logging,traceback
from .auth import *


logger = logging.getLogger(__name__)


@api_view(['POST'])
def login(request):
    try:
        serializer = Login_serializer1(data = request.data)
        if serializer.is_valid():
            auth = authenticate_user(user_name=request.data['user_name'],password=request.data['password'])
            if auth:
                return JsonResponse(
                    {
                        'msg':'Log in successfully',
                        'stat':'Ok'
                    },status=200
                )
            else:
                return JsonResponse(
                    {
                        'msg':'Log in failed',
                        'stat':'Ok'
                    },status=400
                )
                
        else:
            return JsonResponse(
                {
                    'msg':'Log in failed',
                    'stat':'Not Ok',
                    'error':serializer.error_messages
                },status=400
            )
    except Exception as e:
        # logger.error('An error occured %s'+traceback.format_exc())
        print("login error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                'error':str(e),
                'stat':'Not Ok',
                'traceback':str(traceback.format_exc())
            },status=500
        )



@api_view(['POST'])
def user_signin_up(request):
    try:
        input_data = request.data.copy()
        input_data['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        serializer = User_Signup_serializer1(data = input_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'stat':'Ok',
                    'msg':'User created',
                },status=200
            )
        else:
            return Response(
                {
                    'stat':'Not Ok',
                    'msg':'User not created',
                    'error':serializer.errors
                },status=400
            )
    except Exception as e:
        print(" :: user_signin_up :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                'error':str(e),
                'traceback':str(traceback.format_exc()),
                'stat':'Not Ok'
            },status = 500
        )
