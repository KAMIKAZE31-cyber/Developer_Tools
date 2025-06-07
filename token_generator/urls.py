from django.urls import path
from . import views

app_name = 'token_generator'  # Добавляем пространство имен

urlpatterns = [
    path('', views.TokenListView.as_view(), name='home'),
    path('generate/', views.GenerateTokenView.as_view(), name='generate-token'),
    path('delete/<int:token_id>/', views.DeleteTokenView.as_view(), name='delete-token'),
] 