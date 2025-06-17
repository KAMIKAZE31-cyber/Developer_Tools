from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .tools import base64_encode, base64_decode
import sys
import os
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from history_manager import HistoryManager

# Создаем экземпляр HistoryManager
history = HistoryManager('base64_tools_history.json')

@login_required
def base64_tool(request):
    encoded = ''
    decoded = ''
    input_text = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        input_text = request.POST.get('text', '')
        
        logger.debug(f"Received POST request - Action: {action}, Text length: {len(input_text)}")

        if action == 'encode':
            logger.debug("Attempting to encode text")
            encoded = base64_encode(input_text)
            logger.debug(f"Encoded result: {encoded}")
            # Добавляем запись в историю
            history.add_entry("Base64 кодирование", {
                "user": request.user.username,
                "input_length": len(input_text),
                "output_length": len(encoded)
            })
        elif action == 'decode':
            logger.debug("Attempting to decode text")
            decoded = base64_decode(input_text)
            logger.debug(f"Decoded result: {decoded}")
            # Добавляем запись в историю
            history.add_entry("Base64 декодирование", {
                "user": request.user.username,
                "input_length": len(input_text),
                "output_length": len(decoded)
            })

    return render(
        request,
        'tools/base64.html',
        {
            'encoded': encoded,
            'decoded': decoded,
            'input_text': input_text
        }
    )