from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    phone_number     = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.first_name