# base64_tools/urls.py

from django.urls import path
from . import views

app_name = 'base64_tools'  # Добавляем пространство имен

urlpatterns = [
    path('', views.base64_tool, name='home'),
]