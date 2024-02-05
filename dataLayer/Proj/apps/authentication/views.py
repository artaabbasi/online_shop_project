from rest_framework import views, permissions, response, status, generics, decorators
from . import utils, models, serializers, services , docs
import base64
from django.contrib.auth import authenticate
from django.utils import timezone 
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema 
from ..account import serializers as account_serializers

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
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        return response.Response({'detail': "نام کاربری یا رمز عبور اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)

    data = serializers.UserSerializer(user).data
    token = utils.get_tokens_for_user(user)
    data['access'] = token['access']
    data['refresh'] = token['refresh']
    return response.Response(data, status=status.HTTP_200_OK)

@decorators.api_view(['GET', ])
@decorators.permission_classes([permissions.IsAuthenticated, ])
def check(request):
    return response.Response(account_serializers.UserSerializer(request.user).data)