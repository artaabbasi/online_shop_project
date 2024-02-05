from rest_framework import views, permissions, response, status, generics, decorators, viewsets
from . import utils, models, serializers, services , docs, permissions as perms


class UserViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['first_name', 'last_name']
    filter_fields = ['type', 'username']

    def get_queryset(self):
        queryset = self.queryset
        queryset = utils.filter_queryset(queryset=queryset, fields=self.filter_fields, query_params=self.request.query_params)
        queryset = utils.search_queryset(queryset=queryset, fields=self.search_fields, query_params=self.request.query_params)
        return queryset
    

@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.AllowAny, ])
def account_detail(request):
    user_id = request.GET.get('user_id')
    try:
        user_obj = models.User.objects.get(id=user_id)
    except:
        user_obj = None
    return response.Response(serializers.UserSerializer(user_obj).data)