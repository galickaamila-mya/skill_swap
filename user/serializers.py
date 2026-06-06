from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class UserNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "phone", "city", "about", "avatar", "average_rating")
