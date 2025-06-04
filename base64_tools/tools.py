import base64

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    try:
        return base64.b64decode(text).decode()
    except Exception:
        return "Ошибка декодирования"