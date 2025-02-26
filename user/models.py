from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


