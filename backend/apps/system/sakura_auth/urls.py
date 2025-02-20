from django.urls import path
from . import views

app_name = 'sakura_auth'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('token/refresh', views.RefreshView.as_view(), name='refresh')
]