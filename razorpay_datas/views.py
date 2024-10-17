from django.shortcuts import render
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import traceback
from datetime import *

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
            return JsonResponse({"stat": "Ok", "msg": "Data inserted"}, status=200)
        else:
            return JsonResponse(
                {"stat": "Not Ok", "error": serializer.errors}, status=401
            )
    except Exception as e:
        print(
            " :: test credentials error :: "
            + str(e)
            + " :: traceback :: "
            + traceback.format_exc()
        )
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status=500,
        )
