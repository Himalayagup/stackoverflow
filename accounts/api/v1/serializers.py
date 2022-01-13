from rest_framework import serializers
from accounts.models import Token, User
from rest_framework import serializers
from accounts.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)

    name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email',"name")
        extra_kwargs = {
            'name': {'required': True},
        }


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
