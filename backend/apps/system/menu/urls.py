from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'menu'

router = DefaultRouter()
router.register('', views.MenuViewSet, basename='menu')

urlpatterns = [
    path('menu/', include(router.urls))
]