from django.shortcuts import render
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import traceback

# Create your views here.


@api_view(["POST"])
def test_credentials(request):
    try:
        input_data = request.data.copy()
        serializer = Test_credentials_serializers(input=input_data)
        if serializer.is_valid():
            record = Test_credentials.objects.first()
            if record:
                record.key_id = input_data["key_id"]
                record.secret = input_data["secret"]
                record.save()
                return JsonResponse({"stat": "Ok", "msg": "Data updated"}, status=200)
            else:
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
