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

def base64_tool(request):
    result = ""
    if request.method == "POST":
        text = request.POST.get("text", "")
        try:
            result = bytes.fromhex(text).decode('utf-8')
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
    if request.method == 'POST':
        UserHistory.objects.filter(user=request.user).delete()
        messages.success(request, 'История действий очищена')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def text_analyzer(request):
    return render(request, 'tools/text_analyzer.html')

def list_converter(request):
    return render(request, 'tools/list_converter.html')

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