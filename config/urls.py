# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('base64_tool')  # имя маршрута из urls.py или views.py

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),  # ← добавлено
    path('base64/', include('base64_tools.urls')),
]