from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import toml
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('preobrazovarel_history.json')

# Create your views here.

@login_required
def json_to_toml_converter(request):
    result = None
    error = None
    input_format = request.POST.get("input_format", "json")
    input_text = request.POST.get("input_text", "")
    
    if request.method == "POST" and input_text:
        try:
            if input_format == "json":
                # Конвертация из JSON в TOML
                json_data = json.loads(input_text)
                result = toml.dumps(json_data)
                action_type = 'Конвертация JSON в TOML'
            else:
                # Конвертация из TOML в JSON
                toml_data = toml.loads(input_text)
                result = json.dumps(toml_data, indent=2, ensure_ascii=False)
                action_type = 'Конвертация TOML в JSON'
            
            # Добавляем запись в JSON историю
            history.add_entry(action_type, {
                "user": request.user.username,
                "input_length": len(input_text),
                "input_format": input_format,
                "tool_url": '/preobrazovarel/'
            })
            
        except json.JSONDecodeError:
            error = "Ошибка: Неверный формат JSON"
            history.add_entry("Ошибка конвертации", {
                "error": "Неверный формат JSON",
                "user": request.user.username,
                "tool_url": '/preobrazovarel/'
            })
        except toml.TomlDecodeError:
            error = "Ошибка: Неверный формат TOML"
            history.add_entry("Ошибка конвертации", {
                "error": "Неверный формат TOML",
                "user": request.user.username,
                "tool_url": '/preobrazovarel/'
            })
        except Exception as e:
            error = f"Ошибка при конвертации: {str(e)}"
            history.add_entry("Ошибка конвертации", {
                "error": str(e),
                "user": request.user.username,
                "tool_url": '/preobrazovarel/'
            })
    
    return render(request, "preobrazovarel/converter.html", {
        "result": result,
        "error": error,
        "input_format": input_format,
        "input_text": input_text
    })
