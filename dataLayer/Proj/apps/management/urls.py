from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'product', views.ProductViewset)
router.register(r'basket', views.BasketViewset)
router.register(r'basket-product', views.BasketProductViewset)




urlpatterns = [
    path('', include(router.urls)),
]
