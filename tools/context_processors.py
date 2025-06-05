from .models import UserHistory

def user_history(request):
    if request.user.is_authenticated:
        history = UserHistory.objects.filter(user=request.user)[:10]  # Последние 10 действий
    else:
        history = []
    
    return {
        'user_history': history
    } 