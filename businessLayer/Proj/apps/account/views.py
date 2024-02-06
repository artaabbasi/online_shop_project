from rest_framework import views, permissions, response, status, generics, decorators, viewsets
from . import utils, models, serializers, services , docs, permissions as perms



    
@decorators.api_view(['GET'])
@decorators.permission_classes([perms.IsAuthenticated, ])
def account_detail(request):
    return response.Response(request.user_data)