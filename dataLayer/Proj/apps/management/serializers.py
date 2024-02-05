from rest_framework import serializers , response
from . import models
from ..account.serializers import UserRawSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'

class BasketRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Basket
        fields = '__all__'


class BasketProductSerializer(serializers.ModelSerializer):
    product_obj = ProductSerializer(source='product', read_only=True)
    basket_obj = BasketRawSerializer(source='basket', read_only=True)

    class Meta:
        model = models.BasketProduct
        fields = '__all__'
 
class BasketSerializer(serializers.ModelSerializer):
    basket_products = BasketProductSerializer(many=True, read_only=True)
    class Meta:
        model = models.Basket
        fields = '__all__'

