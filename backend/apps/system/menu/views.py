# Create your views here.

from rest_framework import status, viewsets

from utils.response import SuccessResponse
from utils.viewset import CustomViewSet
from .models import Menu
from .serializers import MenuSerializer


class MenuViewSet(CustomViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = None

    def perform_destroy(self, instance):
        instance.meta.delete()
        instance.delete()