from django.shortcuts import render

def base64_tool(request):
    result = ""
    if request.method == "POST":
        text = request.POST.get("text", "")
        try:
            result = bytes.fromhex(text).decode('utf-8')
        except:
            result = "Ошибка декодирования"
    return render(request, "tools/base64.html", {"result": result})