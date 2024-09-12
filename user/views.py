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


logger = logging.getLogger(__name__)


@api_view(['POST'])
def login(request):
    try:
        user_name : str|None = request.data.get("user_name")
        password : str|None = request.data.get("password")
        serializer = Login_serializer1(data = request.data)
        return JsonResponse()
        # if serializer.is_valid():
        #     return JsonResponse(
        #         {
        #             'msg':user_name
        #         }
        #     )
        # else:
        #     return JsonResponse(
        #         {
        #             'error':'seriallizer is not valid'
        #         }
        #     )
    except Exception as e:
        logger.error('An error occured',exc_info=True)
        return JsonResponse(
            {
                'error':str(e),
                'stat':'Not Ok',
            },status=500
        )

