from django.urls import path
from . import views

app_name = 'preobrazovarel'

urlpatterns = [
    path('', views.json_to_toml_converter, name='converter'),
] 