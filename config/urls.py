# config/urls.py

from django.contrib import admin
from django.urls import path, include
from tools.views import ToolsHomeView, register
from django.contrib.auth import views as auth_views
from tools import views as tools_views
from django.shortcuts import redirect
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('register') if not request.user.is_authenticated else redirect('tools_home'), name='root'),
    path('tools/', ToolsHomeView.as_view(), name='tools_home'),
    path('tokens/', include('token_generator.urls')),
    path('base64/', include('base64_tools.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='tools/login.html',
        next_page='tools_home'
    ), name='login'),
    path('logout/', tools_views.logout_view, name='logout'),
    path('register/', tools_views.register, name='register'),
    path('clear-history/', tools_views.clear_history, name='clear_history'),
]