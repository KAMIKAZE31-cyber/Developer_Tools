from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Token
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('token_generator_history.json')

# Create your views here.

class TokenListView(LoginRequiredMixin, ListView):
    model = Token
    template_name = 'token_generator/token_list.html'
    context_object_name = 'tokens'
    ordering = ['-created_at']

    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)

class GenerateTokenView(LoginRequiredMixin, View):
    def post(self, request):
        token = Token.generate_token(user=request.user)
        messages.success(request, f'Новый токен сгенерирован: {token.token}')
        
        # Добавляем запись в JSON историю
        history.add_entry("Генерация токена", {
            "user": request.user.username,
            "token_preview": token.token[:8],
            "created_at": token.created_at.isoformat(),
            "tool_url": '/tokens/'
        })
        
        return redirect('token_generator:home')

    def get(self, request):
        return redirect('token_generator:home')

class DeleteTokenView(LoginRequiredMixin, View):
    def post(self, request, token_id):
        token = get_object_or_404(Token, id=token_id, user=request.user)
        token_preview = token.token[:8]
        token.delete()
        
        # Добавляем запись в JSON историю
        history.add_entry("Удаление токена", {
            "user": request.user.username,
            "token_preview": token_preview,
            "deleted_at": token.created_at.isoformat(),
            "tool_url": '/tokens/'
        })
        
        messages.success(request, 'Токен успешно удален')
        return redirect('token_generator:home')
