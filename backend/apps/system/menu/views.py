# Create your views here.

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

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        return self.queryset.filter(meta__title__icontains=name)