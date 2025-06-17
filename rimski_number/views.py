from django.shortcuts import render
from django.http import JsonResponse
from tools.models import UserHistory
from django.contrib.auth.decorators import login_required
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('rimski_number_history.json')

def to_roman(number):
    if not 0 < number < 4000:
        return "Число должно быть от 1 до 3999"
    
    roman_values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]
    
    result = ""
    for value, numeral in roman_values:
        while number >= value:
            result += numeral
            number -= value
    return result

@login_required
def roman_converter(request):
    return render(request, 'rimski_number/index.html')

@login_required
def convert_number(request):
    try:
        number = int(request.POST.get('number', 0))
        if 0 < number < 4000:
            result = to_roman(number)
            
            # Записываем действие в историю
            UserHistory.objects.create(
                user=request.user,
                action_type='Конвертация в римские цифры',
                details=f'Число {number} преобразовано в {result}'
            )
            
            # Добавляем запись в JSON историю
            history.add_entry("Конвертация в римские цифры", {
                "user": request.user.username,
                "input_number": number,
                "result": result
            })
            
            return JsonResponse({'success': True, 'result': result})
        else:
            error_msg = 'Пожалуйста, введите число от 1 до 3999'
            history.add_entry("Ошибка конвертации", {
                "user": request.user.username,
                "error": error_msg,
                "input_number": number
            })
            return JsonResponse({'success': False, 'error': error_msg})
    except ValueError:
        error_msg = 'Пожалуйста, введите корректное число'
        history.add_entry("Ошибка конвертации", {
            "user": request.user.username,
            "error": error_msg,
            "input": request.POST.get('number', '')
        })
        return JsonResponse({'success': False, 'error': error_msg})
