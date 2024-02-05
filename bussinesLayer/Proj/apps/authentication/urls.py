from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.base_login),
    path('register/', views.register)
]
