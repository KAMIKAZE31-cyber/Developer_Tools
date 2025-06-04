from django.shortcuts import render
from .tools import base64_encode, base64_decode

def base64_tool(request):
    encoded = ''
    decoded = ''

    if request.method == 'POST':
        action = request.POST.get('action')
        text = request.POST.get('text', '')

        if action == 'encode':
            encoded = base64_encode(text)
        elif action == 'decode':
            decoded = base64_decode(text)

    return render(
        request,
        'tools/base64.html',
        {
            'encoded': encoded,
            'decoded': decoded
        }
    )