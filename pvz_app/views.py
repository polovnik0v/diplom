import requests
import json
from django.shortcuts import render

def chat_view(request):
    response_text = ""
    prompt = ""
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        print(prompt)
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "owl/t-lite",  # Замените на используемое название модели, если необходимо
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            # Делаем запрос без streaming, чтобы дождаться полного ответа
            api_response = requests.post(url, json=payload)
            print(api_response.status_code)
            print(api_response.text)
            if api_response.status_code == 200:
                # Разбиваем полученный текст по строкам, фильтруем пустые и сразу собираем итоговый ответ
                response_text = "".join(
                    json.loads(line)["message"]["content"]
                    for line in api_response.text.strip().splitlines()
                    if line.strip()
                )
                print("Итоговый ответ:", response_text)
            else:
                response_text = f"Ошибка: {api_response.status_code}\n{api_response.text}"
        except Exception as e:
            response_text = f"Исключение: {str(e)}"
    return render(request, "pvz_app/chat.html", {"response_text": response_text, "prompt": prompt})
