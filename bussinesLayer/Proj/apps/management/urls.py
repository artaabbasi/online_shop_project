from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter





urlpatterns = [
    path('product/', views.product_list),
    path('product/<int:id>/', views.product_detail),
    path('basket/', views.basket_list),
    path('basket/<int:id>/', views.basket_detail),
    path('basket/basket-product/add/<int:basket_id>/', views.basket_product_add),
    path('basket/basket-product/<int:id>/', views.basket_product_detail)
]
