from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserRetrieveApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
