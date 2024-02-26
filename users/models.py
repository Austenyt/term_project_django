from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='страна', blank=True, null=True)
    is_not_blocked = models.BooleanField(default=True, verbose_name='неблокирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

#     @property
#     def has_view_user_list_permission(self):
#         return self.has_perm('your_app.view_user_list')
#
#
# content_type = ContentType.objects.get_for_model(User)
# permission = Permission.objects.create(
#     codename='view_user_list',
#     name='Can view list of users',
#     content_type=content_type,
# )
