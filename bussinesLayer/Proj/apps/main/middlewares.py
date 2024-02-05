import requests
from django.http import HttpResponseForbidden
import json
from decouple import config
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            header_value = request.headers.get('Authorization')
            auth_api = config('DATA_GATEWAY')
            url = auth_api+'/authentication/check/'
            if header_value:
                headers = {
                    "Authorization":header_value
                }
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    content = response.content
                    data = json.loads(content)
                    request.user_data = data
                    return self.get_response(request)
                else:
                    return HttpResponseForbidden()
            else:
                return self.get_response(request)
        except Exception as e:
            return self.get_response(request)
