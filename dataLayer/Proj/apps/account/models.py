from django.db import models
from django.contrib.auth.models import AbstractUser
from Proj.settings.base import AUTH_USER_MODEL


class User(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "Admin"
        CUSTOMER = "Customer"
        OPERATOR = "Operator"



    type = models.CharField( max_length=50, choices=Types.choices, help_text='ADMIN = "Admin"    CUSTOMER = "Customer"    OPERATOR = "Operator"')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.TextField(null=True, blank=True)
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
