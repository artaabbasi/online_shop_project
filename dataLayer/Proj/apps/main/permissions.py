from rest_framework import permissions
from . import models, utils
from ..account.models import User

class IsOperator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type == User.Types.OPERATOR or request.user.type == User.Types.ADMIN


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type == User.Types.ADMIN
    
class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':  
            return True
        return request.user.type == User.Types.ADMIN