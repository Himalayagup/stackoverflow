from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers

from accounts.models import Token, User


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ("key",)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "mobile",
            "status",
        ]
        read_only_fields = ["id", "email"]
