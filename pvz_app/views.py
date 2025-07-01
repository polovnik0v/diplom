import requests
import json
from django.http import JsonResponse
from .rag.faiss_index import find_relevant_chunks

def chat_view(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        prompt = request.POST.get("prompt", "")
        # Получаем релевантные чанки и собираем контекст
        relevant_chunks = find_relevant_chunks(prompt, top_n=5)
        context_text = "\n".join([doc.page_content for doc in relevant_chunks])
        full_prompt = f"""Ты старший сотрудник пункта выдачи заказов и ты являешься наставником для сотрудника.\n
                            Используй официальный стиль общения.
                            Кратко и понятно объясни, что ему необходимо сделать для ответа на вопрос:{prompt}\n
                            Используя следующую информацию:\n{context_text}"""

        url = "http://localhost:11434/api/chat" 
        response_text = ""
        try:
            api_response = requests.post(
                url,
                json={
                    "model": "owl/t-lite",
                    "messages": [{"role": "user", "content": full_prompt}]
                },
                stream=True
            )
            if api_response.status_code == 200:
                print(api_response)
                for line in api_response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            json_data = json.loads(line)
                            if "message" in json_data and "content" in json_data["message"]:
                                response_text += json_data["message"]["content"]
                        except json.JSONDecodeError:
                            response_text += f"\nОшибка парсинга: {line}"
            else:
                response_text = f"Ошибка: {api_response.status_code}\n{api_response.text}"
        except Exception as e:
            response_text = f"Исключение: {str(e)}"
        return JsonResponse({"response_text": response_text})
    