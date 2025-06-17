from django.urls import path
from . import views

app_name = 'color_HTML'

urlpatterns = [
    path('', views.hex_color, name='hex_color'),
] 