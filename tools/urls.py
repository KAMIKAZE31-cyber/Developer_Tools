from django.urls import path
from . import views

app_name = 'tools'  # Добавляем пространство имен

urlpatterns = [
    path('', views.ToolsHomeView.as_view(), name='home'),
    path('base64/', views.base64_tool, name='base64_tool'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('text-analyzer/', views.text_analyzer, name='text_analyzer'),
    path('list-converter/', views.list_converter, name='list_converter'),
    path('list-converter/save-action/', views.save_list_converter_action, name='save_list_converter_action'),
]