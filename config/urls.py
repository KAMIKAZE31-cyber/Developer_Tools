# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('tools:register') if not request.user.is_authenticated else redirect('tools:home'), name='root'),
    path('tools/', include('tools.urls', namespace='tools')),
    path('passwords/', include('password_generator.urls', namespace='password_generator')),
    path('base64_tools/', include('base64_tools.urls', namespace='base64_tools')),
    path('rimski_number/', include('rimski_number.urls', namespace='rimski_number')),
    path('preobrazovarel/', include('preobrazovarel.urls', namespace='preobrazovarel')),
    path('colors/', include('color_HTML.urls', namespace='color_HTML')),
]