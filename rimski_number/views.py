from django.shortcuts import render
from django.http import JsonResponse
from tools.models import UserHistory
from django.contrib.auth.decorators import login_required

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
            
            return JsonResponse({'success': True, 'result': result})
        else:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, введите число от 1 до 3999'})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Пожалуйста, введите корректное число'})
