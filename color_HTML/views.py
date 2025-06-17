from django.shortcuts import render
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('color_HTML_history.json')

# Create your views here.

def hex_color(request):
    if request.method == 'POST':
        color = request.POST.get('color', '')
        history.add_entry("Генерация цвета", {
            "color": color,
            "method": "POST"
        })
    return render(request, 'color_HTML/hex_color.html')
