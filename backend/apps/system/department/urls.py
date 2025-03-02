from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'department'

router = DefaultRouter()
router.register('', views.DepartmentViewSet, basename='department')

urlpatterns = [
    path('department/', include(router.urls))
]