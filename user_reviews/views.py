from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from .serializers import *
import traceback



@api_view(['POST'])
def post_reviews(request):
    try:
        input_data = request.data.copy()
        serializer = User_review_serializers(data=input_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "stat":"Ok",
                    "msg":"Review posted successfully"
                },status=200
            )
        else:
            return JsonResponse(
                {
                    "stat":"Not Ok",
                    "msg":"Review not posted",
                    "error":serializer.errors
                },status=401
            )

    except Exception as e:
        print(":: post reviews error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=500
        )


@api_view(['POST'])
def get_reviews_by_turf_id(request):
    try:
        input_data = request.data.copy()
        turf_id = input_data.get("turf_id",None)
        if turf_id is None:
            return JsonResponse(
                {
                    "stat":"Not Ok",
                    "msg":"please provide turf id"
                },status = 401
            )
        get_data = User_reviews.objects.filter(turf_ids = turf_id)
        data = list(get_data.values('turf_ids', 'user_name', 'review_message', 'review_starts'))
        df1 = pd.DataFrame(data)
        return JsonResponse(
            {
                "stat":"Ok",
                "data":df1.to_dict(orient="records")
            },status = 200
        )
    except get_data.DoesNotExist:
        return JsonResponse(
            {
                "stat":"Not Ok",
                "msg":f"No data found for this turf id : {turf_id}"
            },status = 200
        )
    except Exception as e:
        print(" :: get reviews by turf id error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return JsonResponse(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=500
        )