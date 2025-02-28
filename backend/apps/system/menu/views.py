# Create your views here.

from rest_framework import status, viewsets

from utils.response import SuccessResponse
from .models import Menu
from .serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        resp_data = super().list(request, *args, **kwargs)
        return SuccessResponse(data=resp_data.data)

    def retrieve(self, request, *args, **kwargs):
        resp_data = super().retrieve(request, *args, **kwargs)
        return SuccessResponse(data=resp_data.data)