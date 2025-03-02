from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'role'

router = DefaultRouter()
router.register('', views.RoleViewSet, basename='role')

urlpatterns = [
    path('role/', include(router.urls)),
]