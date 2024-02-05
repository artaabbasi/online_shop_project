from rest_framework import views, permissions, response, status, generics, decorators
from . import utils, models, serializers, services , docs
import base64
from django.contrib.auth import authenticate
from django.utils import timezone 
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema 
from decouple import config
import requests
import json

# @swagger_auto_schema(operation_description= docs.base_login ,methods=['post'],tags=['authentication'])
@decorators.api_view(['POST', ])
@decorators.permission_classes([permissions.AllowAny, ])
def base_login(request):
    """
    {
        "username":,
        "password":
    }
    """
    auth_api = config('DATA_GATEWAY')
    url = auth_api+'/authentication/login/'
    res = requests.post(url, data=request.data)
    data = json.loads(res.content)
    return response.Response(data, status=res.status_code)


@decorators.api_view(['POST', ])
@decorators.permission_classes([permissions.AllowAny, ])
def register(request):
    """
    {
        "username":,
        "password":,
        "phone_number":,
        "email":,
        "national_id":,
        "home_address":
    }
    """
    auth_api = config('DATA_GATEWAY')
    url = auth_api+'/account/user/'
    data = request.data
    try:
        data['username']
        data['password']
    except:
        return response.Response({"detail":"You should send username and password"}, status=status.HTTP_400_BAD_REQUEST)
    
    check_res = requests.get(url+f"?username={data['username']}", data=data)
    check_data = json.loads(check_res.content)
    if check_data.get('count', 0) > 0:
        return response.Response({"detail":"username duplicated"}, status=status.HTTP_400_BAD_REQUEST)

    data.update({"type":"Customer"})
    res = requests.post(url, data=data)
    data = json.loads(res.content)
    return response.Response(data, status=res.status_code)