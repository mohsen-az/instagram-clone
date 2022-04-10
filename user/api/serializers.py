from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    privacy = serializers.CharField(source="get_privacy_display")

    class Meta:
        model = User
        fields = [
            "username", "email",
            "phone_number", "avatar",
            "bio", "privacy",
            "website", "is_verified"
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "email",
            "phone_number", "avatar",
            "bio", "privacy",
            "website", "is_verified"
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "avatar"]
