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
import time
import random
from datetime import datetime



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
            },status = 200
        )
    except Exception as e:
        print(":: Show turf list error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":str(e),
            },status = 500
        )
    
@api_view(['POST'])
def booking(request):
    try:
        input_data = request.data.copy()
        booking_id = str(random.randint(0000,9999))+str(int(time.time()))
        booking_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        input_data["booking_id"] = booking_id
        input_data["booking_date_time"] = booking_date_time
        input_data["payment_status"] = "pending"
        input_data["temp_lock"] = "LOCKED"
        serializer = Booking_serializer(data = input_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "stat":"Ok",
                    "msg":"slot locked",
                    "booking_id":booking_id
                },status = 200
            )
        else:
            return JsonResponse(
                {
                    "stat":"Not Ok",
                    "error":serializer.errors,
                    "msg":"slot not locked"
                },status = 401
            )
    except Exception as e:
        print(" :: booking error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=500
        )
    
@api_view(['POST'])
def lock_release(request):
    try:
        input_data = request.data.copy()
        booking_id_input = input_data.get("booking_id",None)
        if booking_id_input is None or booking_id_input == "" :
            return JsonResponse(
                {
                    "stat":"Not Ok",
                    "error":"give correct booking id"
                },status = 401
            )
        booking_obj = Booking.objects.get(booking_id = booking_id_input)
        booking_obj.delete()
        return JsonResponse(
            {
                "stat":"Ok",
                "msg":"slot released"
            },status = 200
        )
    except booking_obj.DoesNotExist:
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":"slot not found"
            },status = 401
        )
    except Exception as e:
        print(" :: lock release error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status = 500
        )

