from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserHistory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def base64_tool(request):
    result = ""
    if request.method == "POST":
        text = request.POST.get("text", "")
        try:
            result = bytes.fromhex(text).decode('utf-8')
            # Записываем действие в историю
            UserHistory.objects.create(
                user=request.user,
                action_type='Base64 декодирование',
                details=f'Декодирование текста длиной {len(text)} символов'
            )
        except:
            result = "Ошибка декодирования"
    return render(request, "tools/base64.html", {"result": result})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error': 'Пользователь с таким именем уже существует'})
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('tools:home')
    
    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tools:home')
        else:
            return render(request, 'registration/login.html', {'error': 'Неверное имя пользователя или пароль'})
    
    return render(request, 'registration/login.html')

@login_required
def home_view(request):
    return render(request, 'home.html', {'username': request.user.username})

class ToolsHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'tools/home.html'
    login_url = 'tools:login'

    def handle_no_permission(self):
        messages.warning(self.request, 'Пожалуйста, войдите в систему для доступа к инструментам.')
        return super().handle_no_permission()

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('tools:home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserCreationForm()
    return render(request, 'tools/register.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('tools:home')
    return render(request, 'tools/logout.html')

@login_required
def clear_history(request):
    if request.method == "POST":
        UserHistory.objects.filter(user=request.user).delete()
        messages.success(request, 'История успешно очищена')
    return redirect('tools:home')

@login_required
def text_analyzer(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        if text:
            # Анализ текста
            word_count = len(text.split())
            char_count = len(text)
            line_count = len(text.splitlines())
            
            result = {
                "word_count": word_count,
                "char_count": char_count,
                "line_count": line_count
            }
            
            # Записываем действие в историю
            UserHistory.objects.create(
                user=request.user,
                action_type='Анализ текста',
                details=f'Проанализирован текст: {word_count} слов, {char_count} символов, {line_count} строк'
            )
    
    return render(request, "tools/text_analyzer.html", {"result": result})

@login_required
def list_converter(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        format_type = request.POST.get("format", "bullet")
        
        if text:
            lines = text.splitlines()
            if format_type == "bullet":
                result = "\n".join([f"• {line}" for line in lines if line.strip()])
            elif format_type == "numbered":
                result = "\n".join([f"{i}. {line}" for i, line in enumerate(lines, 1) if line.strip()])
            elif format_type == "dashed":
                result = "\n".join([f"- {line}" for line in lines if line.strip()])
            
            # Записываем действие в историю
            UserHistory.objects.create(
                user=request.user,
                action_type='Конвертация списка',
                details=f'Преобразование текста в формат {format_type}, {len(lines)} строк'
            )
    
    return render(request, "tools/list_converter.html", {"result": result})

@csrf_exempt
@login_required
def save_list_converter_action(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            text = data.get('text')
            result = data.get('result')
            
            action_descriptions = {
                'lowercase': 'Преобразование в нижний регистр',
                'uppercase': 'Преобразование в верхний регистр',
                'capitalize': 'Каждое слово с большой буквы',
                'sentence': 'Каждое предложение с большой буквы',
                'commas': 'Добавление запятых после слов',
                'remove-spaces': 'Удаление пробелов',
                'trim-lines': 'Удаление пробелов в начале и конце строк'
            }
            
            description = f"{action_descriptions.get(action, 'Неизвестное действие')}"
            
            # Сохраняем действие в историю
            UserHistory.objects.create(
                user=request.user,
                action=description,
                input_data=text[:100] if text else '',  # Сохраняем только первые 100 символов
                output_data=result[:100] if result else ''  # Сохраняем только первые 100 символов
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})