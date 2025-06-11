from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tools.models import UserHistory
import json
import toml

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
            
            # Записываем действие в историю
            UserHistory.objects.create(
                user=request.user,
                action_type=action_type,
                details=f'Преобразован текст длиной {len(input_text)} символов'
            )
        except json.JSONDecodeError:
            error = "Ошибка: Неверный формат JSON"
        except toml.TomlDecodeError:
            error = "Ошибка: Неверный формат TOML"
        except Exception as e:
            error = f"Ошибка при конвертации: {str(e)}"
    
    return render(request, "preobrazovarel/converter.html", {
        "result": result,
        "error": error,
        "input_format": input_format,
        "input_text": input_text
    })
