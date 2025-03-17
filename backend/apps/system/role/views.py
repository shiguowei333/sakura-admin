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

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        code = self.request.query_params.get('code', '')
        return self.queryset.filter(name__icontains=name, code__icontains=code)