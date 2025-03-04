from django.shortcuts import render
from rest_framework import viewsets

from utils.viewset import CustomViewSet
from .models import Role
from .serializers import RoleSerializer


# Create your views here.

class RoleViewSet(CustomViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = None