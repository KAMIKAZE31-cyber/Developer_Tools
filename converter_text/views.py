from django.shortcuts import render
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('converter_text_history.json')

def text_converter(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        operation = request.POST.get('operation', '')
        
        # Добавляем запись в историю
        history.add_entry("Конвертация текста", {
            "operation": operation,
            "text_length": len(text)
        })
        
    return render(request, 'converter_text/converter.html')
