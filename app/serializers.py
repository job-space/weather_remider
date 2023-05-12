from django.contrib.auth.models import User

from rest_framework import serializers

from .models import City


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "username", "email"


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "name", "notification_interval", "user"

