from django.shortcuts import render
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import traceback
from datetime import *
from rest_framework import status
import logging
logger = logging.getLogger('django')

# Create your views here.


@api_view(["POST"])
def test_credentials(request):
    try:
        input_data = request.data.copy()
        input_data["saved_date_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = Test_credentials_serializers(data=input_data)
        if serializer.is_valid():
            Test_credentials.objects.all().update(active_status="NO")
            serializer.save()
            return JsonResponse({"stat": "Ok", "msg": "Data inserted"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                {"stat": "Not Ok", "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        logger.error("Error in test credentials :: %s",e,exc_info=True)
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def live_credentials(request):
    try:
        input_data = request.data.copy()
        input_data["saved_date_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = Live_credentials_serializers(data=input_data)
        if serializer.is_valid():
            live_credentials.objects.all().update(active_status="NO")
            serializer.save()
            return JsonResponse({"stat": "Ok", "msg": "Data inserted"}, status.HTTP_200_OK)
        else:
            return JsonResponse(
                {"stat": "Not Ok", "error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        logger.error("Error in live credentials :: %s",e,exc_info=True)
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
