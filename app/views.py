from django.contrib.auth.models import User

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics

from .models import City
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, CitySerializer


class UserAPIList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class CityAPIList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated,)


class CityAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class CityAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
