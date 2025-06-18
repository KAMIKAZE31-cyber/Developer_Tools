from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .tools import base64_encode, base64_decode
import sys
import os
import logging
from django.http import JsonResponse
import base64
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Настройка логирования
logger = logging.getLogger(__name__)

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_history_file_path():
    """Получает путь к файлу истории"""
    history_dir = 'history_files'
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    return os.path.join(history_dir, 'base64_tools_history.json')

def add_to_history(action, text, result, additional_info=None):
    """Добавляет запись в историю"""
    history_file = get_history_file_path()
    
    # Читаем текущую историю
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    # Создаем новую запись
    entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'text': text,
        'result': result
    }
    
    # Добавляем дополнительную информацию, если она есть
    if additional_info:
        entry.update(additional_info)
    
    # Добавляем запись в историю
    history.append(entry)
    
    # Сохраняем обновленную историю
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def delete_from_history(timestamp):
    """Удаляет запись из истории по временной метке"""
    history_file = get_history_file_path()
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    
    # Фильтруем историю, исключая запись с указанной временной меткой
    history = [entry for entry in history if entry['timestamp'] != timestamp]
    
    # Сохраняем обновленную историю
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return True

def clear_history():
    """Очищает всю историю"""
    history_file = get_history_file_path()
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def base64_view(request):
    if request.method == "DELETE":
        if request.GET.get('clear') == 'true':
            if clear_history():
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'error': 'Не удалось очистить историю'}, status=500)
        
        timestamp = request.GET.get('timestamp')
        if not timestamp:
            return JsonResponse({'error': 'Не указана временная метка'}, status=400)
        
        if delete_from_history(timestamp):
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Не удалось удалить запись'}, status=500)
    
    if request.method == "POST":
        action = request.POST.get('action')
        text = request.POST.get('text', '').strip()
        
        if not action:
            return JsonResponse({'error': 'Не указано действие (кодирование/декодирование)'}, status=400)
        
        if not text:
            return JsonResponse({'error': 'Введите текст для обработки'}, status=400)
        
        try:
            if action == 'encode':
                # Кодирование в Base64
                result = base64.b64encode(text.encode()).decode()
                add_to_history(
                    action='encode',
                    text=text,
                    result=result,
                    additional_info={
                        'operation': 'Кодирование',
                        'input_type': 'Текст',
                        'output_type': 'Base64'
                    }
                )
                return JsonResponse({'result': result})
            
            elif action == 'decode':
                # Декодирование из Base64
                try:
                    result = base64.b64decode(text.encode()).decode()
                    add_to_history(
                        action='decode',
                        text=text,
                        result=result,
                        additional_info={
                            'operation': 'Декодирование',
                            'input_type': 'Base64',
                            'output_type': 'Текст'
                        }
                    )
                    return JsonResponse({'result': result})
                except Exception as e:
                    return JsonResponse({'error': 'Некорректная строка Base64'}, status=400)
            
            elif action == 'copy':
                # Запись в историю при копировании
                add_to_history(
                    action='copy',
                    text=text,
                    result=text,
                    additional_info={
                        'operation': 'Копирование',
                        'input_type': 'Текст',
                        'output_type': 'Текст'
                    }
                )
                return JsonResponse({'status': 'success'})
            
            else:
                return JsonResponse({'error': 'Неизвестное действие'}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Читаем историю для отображения
    history_file = get_history_file_path()
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    return render(request, 'tools/base64.html', {'history': history})