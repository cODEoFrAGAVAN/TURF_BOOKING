from django.shortcuts import render
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime,timedelta
from user.auth import user_secret_key
import traceback
import json
import random
import jwt
# import os

turf_images_location = './static/turf_images/'
turf_images_location_for_db = 'static/turf_images/'

@api_view(['POST'])
def turf_registration(request):
    try:
        # print("Current working directory:", os.getcwd())
        input_data = request.data.copy()
        input_data["registration_date"] = datetime.now().strftime("%Y-%m-%d")
        turf_images = request.FILES.getlist('turf_images')
        turf_images_dict = {}
        for i in range(len(turf_images)):
            with open(f'{turf_images_location}{turf_images[i].name}', 'wb+') as destination:
                turf_images_dict[f"{i+1}"] = str(turf_images_location_for_db+turf_images[i].name)
                for chunk in turf_images[i].chunks():
                    destination.write(chunk)
                    
        if 'turf_images' in input_data:
            del input_data['turf_images']
        # print("turf_images_dict :: ",turf_images_dict)
        input_data['turf_images_path'] = json.dumps(turf_images_dict)
        input_data['turf_ids'] = datetime.now().strftime('%d%m%Y%H%M%S')
        serializer = Turf_registration_serializers(data = input_data)
        data_dict = dict()
        if serializer.is_valid():
            serializer.save()
            data_dict['user_name'] = input_data['user_name']
            data_dict['turf_mobile_number'] = input_data['turf_mobile_number']
            data_dict['random_token'] = str(user_secret_key())
            serializer1 = Random_token_seriallizer1(data = data_dict)
            if serializer1.is_valid():
                serializer1.save()
                return Response(
                    {
                        'stat':'Ok',
                        'msg':'Turf registered successfully'
                    },status=200
                )
            else:
                delete_data = Turf_registration.objects.get(user_name = input_data['user_name'],turf_mobile_number=input_data['turf_mobile_number'])
                delete_data.delete()
                return Response(
                    {
                        'stat':'Not Ok',
                        'msg':'Turf not registered',
                        'error':serializer1.errors
                    },status=400
                )
        else:
            return Response(
                {
                    'stat':'Not Ok',
                    'msg':'Turf not registered',
                    'error':serializer.errors
                },status=400
            )    
    except Exception as e:
        print(":: turf_registration error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                'stat':'Not Ok',
                'error':str(e),
                'traceback':str(traceback.format_exc())
            },status=500
        )
        


@api_view(['POST'])
def checking(request):
    try:
        files = request.FILES.getlist('files')
        for i in range(len(files)):
            with open(f'{files[i].name}', 'wb+') as destination:
                    for chunk in files[i].chunks():
                        destination.write(chunk)
        desc = request.data.get('desc')
        print(desc)
        return Response('Ok')
    except Exception as e:
        return Response(
            {
                'stat':'Not Ok',
                'error':str(e),
                'traceback':str(traceback.format_exc())
            }
        )

@api_view(['POST'])
def forget_password(request):
    try:
        input_data = request.data.copy()
        existing_data = Turf_registration.objects.get(user_name = input_data['user_name'])
        print("existing_data :: ",existing_data)
        random_number = random.randint(100000, 999999)
        input_data['otp'] = str(random_number)
        input_data['mobile_number'] = existing_data.turf_mobile_number
        input_data['mailid'] = existing_data.turf_mailid
        input_data['isvalid'] = 'True'
        serializer = Forget_turf_password_serializers(data = input_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'stat':'Ok',
                    'otp':str(random_number),
                    'msg':'otp sent to your register mobile number and mailid'
                }
            )
        else:
            return Response(
                {
                    'stat':'Not Ok',
                    'error':serializer.errors,
                    'msg':'otp not sent'
                },status=401
            )
    except Exception as e:
        print(":: forget password error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                'stat':'Not Ok',
                'error':str(e),
                'traceback':traceback.format_exc()
            },status=500
        )

@api_view(['POST'])
def check_otp(request):
    try:
        input_data = request.data.copy()
        user_name = input_data.get('user_name',None)
        otp = input_data.get('otp',None)
        if user_name is None or otp is None:
            return Response(
                {
                    'stat':'Not Ok',
                    'error':'give correct credentials'
                },status=401
            )
        check_data = Forget_turf_password.objects.get(user_name = user_name,otp = otp)
        if check_data.user_name == user_name and check_data.otp == otp:
            return Response(
                {
                    'stat':'Ok',
                    'msg':'otp matched'
                },status=200
            )
        else:
            return Response(
                {
                    'stat':'Not Ok',
                    'msg':'otp not mathced with this user name'
                },status=401
            )
    except Forget_turf_password.DoesNotExist:
        return Response(
                {
                    'stat':'Not Ok',
                    'msg':'otp not valid'
                },status=401
            )
    except Exception as e:
        print(" :: check_otp :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                'stat':'Not Ok',
                'error':str(e),
                'traceback':str(traceback.format_exc())
            },status=500
        )

@api_view(['POST'])
def update_password(request):
    try:
        input_data = request.data.copy()
        user_name = input_data.get('user_name',None)
        otp = input_data.get('otp',None)
        new_password = input_data.get('new_password',None)
        saved_otp = Forget_turf_password.objects.get(user_name = user_name,otp = otp,isvalid = 'True')
        saved_otp.isvalid = 'False'
        saved_otp.save()
        update_pass = Turf_registration.objects.get(user_name=user_name)
        update_pass.password = new_password
        update_pass.save()
        return Response(
            {
                "stat":"Ok",
                "msg":"Password updated successfully"
            },status=200
        )
    except Forget_turf_password.DoesNotExist:
        return Response(
            {
                'stat':'Not Ok',
                'error':'otp not mathced with this user name'
            },status=401
        )
    except Turf_registration.DoesNotExist:
        return Response(
            {
                'stat':'Not Ok',
                'error':"user doesn't exists"   
            },status=401
        )
    except Exception as e:
        print(" :: update password error :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                'stat':'Not Ok',
                'error':str(e),
                'traceback':str(traceback.format_exc())
            },status=500
        )

@api_view(['POST'])
def turf_user_login(request):
    try:
        input_data = request.data.copy()
        user_name = input_data.get("user_name",None)
        password = input_data.get("password",None)
        if user_name is None or password is None:
            return Response(
                {
                    'stat':'Not Ok',
                    'error':'give valid credentials'
                },status=401
            )
        user = Turf_registration.objects.get(user_name = user_name,password = password)
        if user:
            expired_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            secret_key = Random_token_generation.objects.get(user_name=user.user_name)
            payload = {
                    "date": user.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "user_name": user.user_name,
                    "password": user.password,
                    "exp_time": expired_time,
                }
            encoded = jwt.encode(payload, (secret_key.random_token), algorithm="HS256")
            return JsonResponse(
                    {"msg": "Log in successfully", "stat": "Ok", "token": encoded},
                    status=200,
                )
        else:
            return JsonResponse({"msg": "Log in failed", "stat": "Ok"}, status=400)
    except Exception as e:
        print(":: turf login error ::"+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                'stat':'Not Ok',
                'error':str(e),
                'traceback':str(traceback.format_exc())
            },status=500
        )

@api_view(['POST'])
def update_turf_deatils(request):
    try:
        input_data = request.data.copy()
        user_name = input_data.get("user_name",None)
        password = input_data.get("password",None)
        update_key = input_data.get("update_key",None)
        # value = input_data.get("value",None)
        # value is None 
        if update_key is None or  user_name is None or password is None or update_key == {}:
            return Response(
                {
                    "stat":"Not Ok",
                    "error":"give correct key and value for updating turf details"
                },status = 401
            )
        else:
            update_details = Turf_registration.objects.get(user_name=user_name,password=password)
            if "turf_name" in update_key:
                update_details.turf_name = update_key["turf_name"]
            if "turf_address" in update_key:
                update_details.turf_address = update_key["turf_address"]
            if "turf_pincode" in update_key:
                update_details.turf_pincode = update_key["turf_pincode"]
            if "tur_land_line_number" in update_key:
                update_details.tur_land_line_number = update_key["tur_land_line_number"]
            if "turf_end_time" in update_key:
                update_details.turf_end_time = update_key["turf_end_time"]
            if "turf_start_time" in update_key:
                update_details.turf_start_time = update_key["turf_start_time"]
            update_details.save()
            return Response(
            {
                "stat":"Ok",
                "msg":"Data updated successfully"
            },status=200
        )
    except Exception as e:
        print(" :: update turf details :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=500
        )
    
@api_view(['POST'])
def update_turf_mobile_number(request):
    try:
        input_data = request.data.copy()
        random_number = random.randint(100000, 999999)
        input_data["otp"] = str(random_number)
        input_data["isvalid"] = "True"
        serializer = Update_turf_mobile_number_serializer1(data = input_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "stat":"Ok",
                    "msg":"Otp sent to new number",
                    "otp":str(random_number)
                },status = 200
            )
        else:
            return Response(
                {
                    'stat':'Not Ok',
                    'error':serializer.errors,
                    'msg':'otp not sent'
                },status=401
            )
    except Exception as e:
        print(" :: update turf mobile :: "+str(e)+" :: traceback :: "+traceback.format_exc())
        return Response(
            {
                "stat":"Not Ok",
                "error":str(e),
                "traceback":str(traceback.format_exc())
            },status=500
        )

