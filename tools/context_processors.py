import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

def user_history(request):
    if request.user.is_authenticated:
        # Получаем историю из всех JSON файлов
        history_files = [
            'tools_history.json',
            'base64_tools_history.json',
            'color_HTML_history.json',
            'token_generator_history.json',
            'rimski_number_history.json',
            'preobrazovarel_history.json'
        ]
        
        all_history = []
        for file_name in history_files:
            history_manager = HistoryManager(file_name)
            user_history = [
                entry for entry in history_manager.get_history()
                if entry.get('details', {}).get('user') == request.user.username
            ]
            all_history.extend(user_history)
        
        # Сортируем по времени и берем последние 10 записей
        all_history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        history = all_history[:10]
    else:
        history = []
    
    return {
        'user_history': history
    } 