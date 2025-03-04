from rest_framework import viewsets

from utils.viewset import CustomViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(CustomViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer