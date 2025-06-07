# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('tools:register') if not request.user.is_authenticated else redirect('tools:home'), name='root'),
    path('tools/', include('tools.urls', namespace='tools')),
    path('tokens/', include('token_generator.urls', namespace='token_generator')),
    path('base64/', include('base64_tools.urls', namespace='base64_tools')),
]