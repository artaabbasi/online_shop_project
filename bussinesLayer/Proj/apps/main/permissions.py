from rest_framework import permissions
from . import models, utils
from ..account.models import User


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(getattr(request, 'user_data', None))   
    

class IsAuthenticatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method=='GET':
            return True
        return bool(getattr(request, 'user_data', None))   
    
class IsPersonnelOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='GET':
            return True
        return utils.is_personnel(request.user_data)
    
class IsPersonnel(permissions.BasePermission):
    def has_permission(self, request, view):
        return utils.is_personnel(request.user_data)