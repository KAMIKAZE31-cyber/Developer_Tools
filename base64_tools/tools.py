import base64

def base64_encode(text):
    try:
        return base64.b64encode(text.encode()).decode()
    except Exception as e:
        return f"Ошибка кодирования: {str(e)}"

def base64_decode(text):
    try:
        return base64.b64decode(text).decode()
    except Exception as e:
        return f"Ошибка декодирования: {str(e)}"