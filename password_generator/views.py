from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Password
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('password_generator_history.json')

# Create your views here.

class PasswordListView(LoginRequiredMixin, ListView):
    model = Password
    template_name = 'password_generator/password_list.html'
    context_object_name = 'passwords'
    ordering = ['-created_at']

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)

class GeneratePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        length = int(request.POST.get('length', 12))
        use_lower = bool(request.POST.get('use_lower'))
        use_upper = bool(request.POST.get('use_upper'))
        use_digits = bool(request.POST.get('use_digits'))
        use_special = bool(request.POST.get('use_special'))
        password = Password.generate_password(
            user=request.user,
            length=length,
            use_lower=use_lower,
            use_upper=use_upper,
            use_digits=use_digits,
            use_special=use_special
        )
        messages.success(request, f'Новый пароль сгенерирован: {password.password}')
        # Добавляем запись в JSON историю
        history.add_entry("Генерация пароля", {
            "user": request.user.username,
            "password_preview": password.password[:8],
            "created_at": password.created_at.isoformat(),
            "tool_url": '/passwords/'
        })
        return redirect('password_generator:home')

    def get(self, request):
        return redirect('password_generator:home')

class DeletePasswordView(LoginRequiredMixin, View):
    def post(self, request, password_id):
        password = get_object_or_404(Password, id=password_id, user=request.user)
        password_preview = password.password[:8]
        password.delete()
        # Добавляем запись в JSON историю
        history.add_entry("Удаление пароля", {
            "user": request.user.username,
            "password_preview": password_preview,
            "deleted_at": password.created_at.isoformat(),
            "tool_url": '/passwords/'
        })
        messages.success(request, 'Пароль успешно удален')
        return redirect('password_generator:home')
