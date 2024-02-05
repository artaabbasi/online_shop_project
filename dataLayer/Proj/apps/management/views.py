from rest_framework import views, permissions, response, status, generics, decorators, viewsets
from . import utils, models, serializers, services , docs, permissions as perms


class ProductViewset(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['name',]
    filter_fields = []

    def get_queryset(self):
        queryset = self.queryset
        queryset = utils.filter_queryset(queryset=queryset, fields=self.filter_fields, query_params=self.request.query_params)
        queryset = utils.search_queryset(queryset=queryset, fields=self.search_fields, query_params=self.request.query_params)
        return queryset

class BasketViewset(viewsets.ModelViewSet):
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = []
    filter_fields = ['user_id', 'status']

    def get_queryset(self):
        queryset = self.queryset
        queryset = utils.filter_queryset(queryset=queryset, fields=self.filter_fields, query_params=self.request.query_params)
        queryset = utils.search_queryset(queryset=queryset, fields=self.search_fields, query_params=self.request.query_params)
        return queryset
    
class BasketProductViewset(viewsets.ModelViewSet):
    queryset = models.BasketProduct.objects.all()
    serializer_class = serializers.BasketProductSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = []
    filter_fields = ['product_id', 'basket_id']

    def get_queryset(self):
        queryset = self.queryset
        queryset = utils.filter_queryset(queryset=queryset, fields=self.filter_fields, query_params=self.request.query_params)
        queryset = utils.search_queryset(queryset=queryset, fields=self.search_fields, query_params=self.request.query_params)
        return queryset