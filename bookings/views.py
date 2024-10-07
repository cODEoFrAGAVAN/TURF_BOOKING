from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from turfs.models import *
import traceback
import pandas as pd
import json



@api_view(['POST'])
def show_turf_list(request):
    try:
        all_turf_list = Turf_registration.objects.all().values("turf_name","turf_address","turf_pincode","turf_mobile_number","turf_images_path","turf_ids","turf_start_time","turf_end_time")
        df = pd.DataFrame(all_turf_list)
        # df["turf_images_path"] = df["turf_images_path"].apply(json.loads)
        df = df.fillna("")
        return JsonResponse(
            {
                "stat":"Ok",
                "data":df.to_dict(orient="records")
            }
        )
    except Exception as e:
        print(":: Show turf list error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":str(e),
            },status = 500
        )