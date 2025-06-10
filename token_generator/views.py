from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Token
from tools.models import UserHistory

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
        
        # Записываем действие в историю
        UserHistory.objects.create(
            user=request.user,
            action_type='Генерация токена',
            details=f'Создан новый токен: {token.token[:8]}...'
        )
        
        return redirect('token_generator:home')

    def get(self, request):
        return redirect('token_generator:home')

class DeleteTokenView(LoginRequiredMixin, View):
    def post(self, request, token_id):
        token = get_object_or_404(Token, id=token_id, user=request.user)
        token_preview = token.token[:8]
        token.delete()
        
        # Записываем действие в историю
        UserHistory.objects.create(
            user=request.user,
            action_type='Удаление токена',
            details=f'Удален токен: {token_preview}...'
        )
        
        messages.success(request, 'Токен успешно удален')
        return redirect('token_generator:home')
