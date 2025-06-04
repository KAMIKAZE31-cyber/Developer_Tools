# base64_tools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.base64_tool, name='base64_tool'),
]