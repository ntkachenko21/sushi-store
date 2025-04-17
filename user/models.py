from django.contrib.auth.models import AbstractUser
from django.db import models

from checkout.models import Cart


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.PROTECT, related_name="user", null=True)
