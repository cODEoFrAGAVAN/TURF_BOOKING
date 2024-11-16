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
from rest_framework import status
import razorpay_datas
from decorators import * 
import logging
import razorpay
from razorpay_datas.models import *
logger = logging.getLogger('django')

def razorpay_client_session():
    try:
        cred = Test_credentials.objects.values("key_id", "secret").get(
                active_status="YES"
            )
        client = razorpay.Client(auth=(cred.Key_id, cred.secret))
        return client
    except Test_credentials.DoesNotExist:
        return False
    except Exception as e:
        logger.error(" Error in razor pay client session creation :: ",e,exc_info=True)
        return False


@api_view(["POST"])
@authorize
def show_turf_list(request):
    try:
        all_turf_list = Turf_registration.objects.all().values(
            "turf_name",
            "turf_address",
            "turf_pincode",
            "turf_mobile_number",
            "turf_images_path",
            "turf_ids",
            "turf_start_time",
            "turf_end_time",
        )
        df = pd.DataFrame(all_turf_list)
        # df["turf_images_path"] = df["turf_images_path"].apply(json.loads)
        df = df.fillna("")
        return JsonResponse(
            {"stat": "Ok", "data": df.to_dict(orient="records")}, status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error("Error in show turf list :: %s",e,exc_info=True)
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def payment_intiate(booking_id, amount):
    try:
        razorpay_client = razorpay_datas.Client(
            auth=("rzp_test_OduFyTcaEnLe6N", "wK80MjEIAc9aPoL2BLUTIOlS")
        )
        # payment_id = booking_id
        data = {"amount": amount, "currency": "INR", "receipt": booking_id,"payment_capture": 1}
        payment = razorpay_client.order.create(data=data)
        return {"stat": "Ok", "payment": payment}
    except Exception as e:
        logger.error("Error in payment initiate function :: %s",e,exc_info=True)
        return {"stat": "Not Ok", "error": str(e)}


@api_view(["POST"])
def booking(request):
    try:
        input_data = request.data.copy()
        booking_id = str(random.randint(0000, 9999)) + str(int(time.time()))
        booking_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        input_data["booking_id"] = booking_id
        input_data["booking_date_time"] = booking_date_time
        input_data["payment_status"] = "PENDING"
        input_data["temp_lock"] = "LOCKED"
        amount = input_data["amount"]
        serializer = Booking_serializer(data=input_data)
        if serializer.is_valid():
            payment_val = payment_intiate(booking_id, int(amount) * 100)
            if payment_val["stat"] == "Not Ok":
                return JsonResponse(
                    {
                        "stat": "Not Ok",
                        "error": payment_val["error"],
                        "msg": "slot not locked",
                    },status=status.HTTP_402_PAYMENT_REQUIRED
                )
            else:
                input_data_1 = dict()
                input_data_1["booking_id"] = booking_id
                input_data_1["payment_id"] = payment_val["payment"]["id"]
                input_data_1["payment_status"] = "PENDING"
                serializer1 = Store_order_id_serializer(data=input_data_1)
                if serializer1.is_valid():
                    serializer.save()
                    serializer1.save()
                    return JsonResponse(
                        {
                            "stat": "Ok",
                            "msg": "slot locked",
                            "booking_id": booking_id,
                            "payment": payment_val["payment"],
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return JsonResponse(
                        {
                            "stat": "Not Ok",
                            "error": serializer1.errors,
                            "msg": "slot not locked",
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        else:
            return JsonResponse(
                {
                    "stat": "Not Ok",
                    "error": serializer.errors,
                    "msg": "slot not locked",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        logger.error("Error in booking :: %s",e,exc_info=True)
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def lock_release(request):
    try:
        input_data = request.data.copy()
        booking_id_input = input_data.get("booking_id", None)
        if booking_id_input is None or booking_id_input == "":
            return JsonResponse(
                {"stat": "Not Ok", "error": "give correct booking id"}, status=status.HTTP_401_UNAUTHORIZED
            )
        booking_obj = Booking.objects.get(booking_id=booking_id_input)
        booking_obj.delete()
        return JsonResponse({"stat": "Ok", "msg": "slot released"}, status=status.HTTP_200_OK)
    except booking_obj.DoesNotExist:
        return JsonResponse({"stat": "Not Ok", "error": "slot not found"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.error("Error in lock release :: %s",e,exc_info=True)
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
                "traceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def verify_payment(request):
    try:
        input_data = request.data.copy()
        razorpay_order_id = input_data.get("razorpay_order_id", None)
        razorpay_payment_id = input_data.get("razorpay_payment_id", None)
        razorpay_signature = input_data.get("razorpay_signature", None)
        signature_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }
        razorpay_datas.razorpay_client.utility.verify_payment_signature(signature_dict)
        payment = razorpay_datas.razorpay_client.payment.fetch(razorpay_payment_id)
        if payment["status"] == "authorized":
            get_data1 = razorpay_datas.razorpay_client.payment.capture(
                razorpay_payment_id, payment["amount"]
            )
            print(get_data1)
            return JsonResponse(
                {"stat": "Ok", "msg": "Payment Verified Successfully"}, status=status.HTTP_200_OK
            )
    except razorpay_datas.errors.SignatureVerificationError:
        return JsonResponse(
            {"stat": "Not Ok", "msg": "Payment Verification Failed"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error("Error in verify payment :: %s",e,exc_info=True)
        return JsonResponse(
            {
                "stat": "Not Ok",
                "error": str(e),
                "trceback": str(traceback.format_exc()),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['POST'])
def via_upi_payment(request):
    try:
        input_data = request.data.copy()
        payment_order_id = input_data["payment_order_id"]
        upi_id = input_data["upi_id"]
        payment_data = {
            "order_id":payment_order_id,
            "method":"upi",
            "upi":{
                "vpa":upi_id
            }
        }
        client = razorpay_client_session()
        if client:
            payment = client.payment.create(payment_data)
            return Response(
                {
                    "stat":"Ok",
                    "payment":payment
                },status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "stat":"Not Ok",
                    "error":"Razor pay client session creation error",
                    "msg":"payment cannot be initated"
                },status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        logger.error("Error in via upi payment :: %s",e,exc_info=True)
        return Response(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )