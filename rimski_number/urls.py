from django.urls import path
from . import views

app_name = 'rimski_number'

urlpatterns = [
    path('', views.roman_converter, name='home'),
    path('convert/', views.convert_number, name='convert'),
] 