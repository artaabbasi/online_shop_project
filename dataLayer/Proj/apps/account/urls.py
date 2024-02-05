from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user', views.UserViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('detail/', views.account_detail)
]
