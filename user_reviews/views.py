from django.shortcuts import render
from rest_framework.response import Response
# from django.http import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from .serializers import *
import traceback
from rest_framework import status
import logging
logger = logging.getLogger('django')



@api_view(["POST"])
def post_reviews(request):
    try:
        input_data = request.data.copy()
        serializer = User_review_serializers(data=input_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"stat": "Ok", "msg": "Review posted successfully"}, status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "stat": "Not Ok",
                    "msg": "Review not posted",
                    "error": serializer.errors,
                },
                status.HTTP_401_UNAUTHORIZED,
            )

    except Exception as e:
        logger.error("Error in post reviews :: %s",e,exc_info=True)
        return Response(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_reviews_by_turf_id(request):
    try:
        input_data = request.data.copy()
        turf_id = input_data.get("turf_id", None)
        if turf_id is None:
            return Response(
                {"stat": "Not Ok", "msg": "please provide turf id"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        get_data = User_reviews.objects.filter(turf_ids=turf_id)
        data = list(
            get_data.values("turf_ids", "user_name", "review_message", "review_starts")
        )
        df1 = pd.DataFrame(data)
        return Response(
            {"stat": "Ok", "data": df1.to_dict(orient="records")},
            status=status.HTTP_200_OK,
        )
    except get_data.DoesNotExist:
        return Response(
            {"stat": "Not Ok", "msg": f"No data found for this turf id : {turf_id}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error("Error in get reviews by turf id :: %s",e,exc_info=True)
        return Response(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def update_review_by_turf_id(request):
    try:
        input_data = request.data.copy()
        serializer = User_review_serializers(data=input_data)
        if serializer.is_valid():
            turf_id = input_data.get("turf_id", None)
            review_messages = input_data.get("review_message", None)
            user_name = input_data.get("user_name", None)
            user_review = User_reviews.objects.get(
                turf_ids=turf_id, user_name=user_name
            )
            user_review.review_message = review_messages
            user_review.save()
            return Response(
                {"stat": "Ok", "msg": "Review updated"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "stat": "Not Ok",
                    "error": serializer.errors,
                    "msg": "Review not updated",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except user_review.DoesNotExist:
        return Response(
            {"stat": "Not Ok", "error": "review not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error("Error in update reviews  :: %s",e,exc_info=True)
        return Response(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
