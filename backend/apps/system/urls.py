from django.urls import path, include

urlpatterns = [
    path('system/', include('apps.system.department.urls')),
    path('system/', include('apps.system.role.urls')),
    path('system/', include('apps.system.user.urls')),
    path('system/', include('apps.system.menu.urls')),
]