from django.shortcuts import render
from django.http import JsonResponse
import logging
from history_manager import HistoryManager

logger = logging.getLogger(__name__)

def hex_color(request):
    if request.method == 'POST':
        try:
            color = request.POST.get('color', '')
            logger.debug(f"Received color: {color}")
            
            history_manager = HistoryManager('color_hex_history.json')
            history_manager.add_entry('color_selected', {'color': color})
            logger.debug("Added color entry to history")
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Color processing error: {e}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'color_HTML/hex_color.html')
