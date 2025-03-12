from django.shortcuts import render
from rest_framework import viewsets

from utils.viewset import CustomViewSet
from .models import Department
from .serializers import DepartmentSerializer


# Create your views here.

class DepartmentViewSet(CustomViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = None

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        if name is None:
            return self.queryset
        return self.queryset.filter(name__icontains=name)