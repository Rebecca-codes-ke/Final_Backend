# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "first_name", "last_name", "role", "is_active"]

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)

#     class Meta:
#         model = User
#         fields = ["username", "email", "first_name", "last_name", "role", "password"]

#     def create(self, validated_data):
#         pwd = validated_data.pop("password")
#         user = User(**validated_data)
#         user.set_password(pwd)
#         user.save()
#         return user

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(
            **validated_data,
            role=User.Role.MERCH,      # ✅ force merchandiser
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(password)
        user.save()
        return user
