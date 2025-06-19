from django.urls import path
from . import views

app_name = 'password_generator'  # Новое пространство имен

urlpatterns = [
    path('', views.PasswordListView.as_view(), name='home'),
    path('generate/', views.GeneratePasswordView.as_view(), name='generate-password'),
    path('delete/<int:password_id>/', views.DeletePasswordView.as_view(), name='delete-password'),
] 