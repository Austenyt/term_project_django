from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    is_not_blocked = models.BooleanField(default=True, verbose_name='неблокирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
