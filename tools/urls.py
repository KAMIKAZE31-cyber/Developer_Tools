from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("base64/", views.base64_tool, name="base64_tool"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home_view, name='home'),
]