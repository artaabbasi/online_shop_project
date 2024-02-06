import json
import requests
from rest_framework import views, permissions, response, status, generics, decorators, viewsets
from . import utils, models, serializers, services , docs, permissions as perms
import base64
from django.contrib.auth import authenticate
from django.utils import timezone 
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema 
from django.core.cache import caches, cache
from decouple import config

@decorators.api_view(['POST', 'GET'])
@decorators.permission_classes([perms.IsAuthenticatedOrReadOnly, perms.IsPersonnelOrReadOnly])
def product_list(request):
    gateway = config('DATA_GATEWAY')
    url = gateway+'/management/product/'
    if request.method == 'GET':
        page = request.GET.get("page", 1)
        size = request.GET.get("size", 30)
        name = request.GET.get("name", )

        cache_key = f'productList_page_{page}_size_{size}_name_{name}'
        cached_data = caches['default'].get(cache_key)

        if cached_data:
            return response.Response(cached_data)

        res = requests.get(url, params=request.GET)
        data = json.loads(res.content)
        if res.status_code == 200:
            caches['default'].set(cache_key, data, timeout=120*60, version=None)
        
        return response.Response(data, status=res.status_code)

    res = requests.post(url, data=request.data)
    data = json.loads(res.content)
    if res.status_code == 201:
        cache = caches['default'] 
        keys_to_delete = cache.client.keys('productList*')
        for key in keys_to_delete:
            cache.delete(key)

    return response.Response(data, status=res.status_code)


@decorators.api_view(['PATCH', 'GET', 'DELETE'])
@decorators.permission_classes([perms.IsAuthenticatedOrReadOnly, perms.IsPersonnelOrReadOnly])
def product_detail(request, id):
    gateway = config('DATA_GATEWAY')
    url = gateway+f'/management/product/{id}/'
    res = requests.request(request.method, url, data=request.data)
    try:
        data = json.loads(res.content)
    except:
        data = res.text
    if request.method != 'GET':
        cache = caches['default'] 
        keys_to_delete = cache.client.keys('productList*')
        for key in keys_to_delete:
            cache.delete(key)
    return response.Response(data, status=res.status_code)

@decorators.api_view(['GET', 'POST'])
@decorators.permission_classes([perms.IsAuthenticated])
def basket_list(request):
    gateway = config('DATA_GATEWAY')
    url = gateway+'/management/basket/'
    bp_url = gateway+'/management/basket-product/'

    if request.method == 'GET':
        page = request.GET.get("page", 1)
        size = request.GET.get("size", 30)
        user_id = request.GET.get("user_id", )
        status = request.GET.get("status", )
        
        if utils.is_personnel(request.user_data):
            user_id = user_id if user_id else request.user_data.get('id')
        else:
            user_id = request.user_data.get('id')
        request_get = dict(request.GET)
        request_get.update({"user_id":user_id})
        cache_key = f'basketList_page_{page}_size_{size}_user_{user_id}_status_{status}'
        cached_data = caches['default'].get(cache_key)

        if cached_data:
            return response.Response(cached_data)

        res = requests.get(url, params=request_get)
        data = json.loads(res.content)
        if res.status_code == 200:
            caches['default'].set(cache_key, data, timeout=120*60, version=None)
        
        return response.Response(data, status=res.status_code)

    data = request.data
    data.update({"user":request.user_data.get('id')})
    basket_product_data = data.pop('basket_products', [])
    res = requests.post(url, data=data)
    data = json.loads(res.content)

    for basket_product_dataum in basket_product_data:
        basket_product_dataum.update({"basket":data.get('id')})
        bp_res = requests.post(bp_url, data=basket_product_dataum)


    if res.status_code == 201:
        cache = caches['default'] 
        keys_to_delete = cache.client.keys('basketList*')
        for key in keys_to_delete:
            cache.delete(key)

    return response.Response(data, status=res.status_code)


@decorators.api_view(['POST'])
@decorators.permission_classes([perms.IsAuthenticated])
def basket_product_add(request, basket_id):
    gateway = config('DATA_GATEWAY')
    url = gateway+'/management/basket-product/'
    data = request.data
    data.update({"basket":basket_id})
    res = requests.post(url, data=data)
    data = json.loads(res.content)
    if res.status_code == 201:
        cache = caches['default'] 
        keys_to_delete = cache.client.keys('basketList*')
        for key in keys_to_delete:
            cache.delete(key)
    return response.Response(data, status=res.status_code)
    

@decorators.api_view(['PATCH', 'DELETE'])
@decorators.permission_classes([perms.IsAuthenticated])
def basket_product_detail(request, id):
    gateway = config('DATA_GATEWAY')
    url = gateway+f'/management/basket-product/{id}'
    res = requests.get(url)
    data = json.loads(res.content)
    request_data = request.data
    if not utils.is_personnel(request.user_data):
        basket_user_id = data.get('basket_obj', {}).get('user')
        if not basket_user_id == request.user_data.get('id'):
            return response.Response({"detail":"You dont have access to this basket."}, status=status.HTTP_403_FORBIDDEN)
        
    res = requests.request(request.method, url, data=request_data)
    try:
        data = json.loads(res.content)
    except:
        data = res.text
    if request.method != 'GET':
        cache = caches['default'] 
        keys_to_delete = cache.client.keys('basketList*')
        for key in keys_to_delete:
            cache.delete(key)
    return response.Response(data, status=res.status_code)

@decorators.api_view(['PATCH', 'DELETE', 'GET'])
@decorators.permission_classes([perms.IsAuthenticated])
def basket_detail(request, id):
    gateway = config('DATA_GATEWAY')
    url = gateway+f'/management/basket/{id}/'
    res = requests.get(url)
    data = json.loads(res.content)
    request_data = request.data
    
    if not utils.is_personnel(request.user_data):
        basket_user_id = data.get('user')
        if not basket_user_id == request.user_data.get('id'):
            return response.Response({"detail":"You dont have access to this basket."}, status=status.HTTP_403_FORBIDDEN)
        
        request_data.update({"status":data.get('status')})

    res = requests.request(request.method, url, data=request_data)
    try:
        data = json.loads(res.content)
    except:
        data = res.text

    if request.method != 'GET':
        cache = caches['default'] 
        keys_to_delete = cache.client.keys('basketList*')
        for key in keys_to_delete:
            cache.delete(key)
    return response.Response(data, status=res.status_code)
    
