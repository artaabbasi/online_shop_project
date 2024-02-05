from django.db import models
from ..account import models as account_models

class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    buy_price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()

class Basket(models.Model):
    class Status(models.IntegerChoices):
        PENDING=1
        ACCEPTED=2
        DECLIEND=3
        SENT=4

    user = models.ForeignKey(account_models.User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING)

    @property
    def basket_products(self):
        return self.basket_product_set.all()
    
class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_product_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(default=0)