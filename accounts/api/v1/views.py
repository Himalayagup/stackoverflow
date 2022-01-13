from django.dispatch import Signal, receiver
# from rest_auth.views import LoginView, LogoutView
from allauth.account import app_settings as allauth_settings
from django.conf import settings
from accounts.models import User
from rest_framework import generics, status
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
