import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token as AuthToken
from django.contrib import auth
STATUS = (
    ("inactive", "Inactive"),
    ("active", "Active"),
)

class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=50)
    status = models.CharField("Account Status",
                              max_length=15,
                              choices=STATUS, default=STATUS[0][0])


class Token(AuthToken):
    key = models.CharField("Key", max_length=40, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name="User",
    )
