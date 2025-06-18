from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('color_HTML_history.json')

# Create your views here.

@login_required
def hex_color(request):
    if request.method == 'POST':
        color = request.POST.get('color', '')
        # Добавляем запись в JSON историю
        history.add_entry("Выбор цвета", {
            "user": request.user.username,
            "color": color,
            "method": "POST",
            "tool_url": '/color_HTML/'
        })
        return JsonResponse({'status': 'success'})
    
    # Получаем историю цветов
    color_history = history.get_history(limit=10)
    return render(request, 'color_HTML/hex_color.html', {
        'color_history': color_history
    })
