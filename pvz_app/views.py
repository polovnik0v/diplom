# import requests
# import json
# from django.shortcuts import render
# from .rag.faiss_index import find_relevant_chunks

# def chat_view(request):
#     response_text = ""
#     prompt = ""
#     if request.method == "POST":
#         prompt = request.POST.get("prompt", "")
#         # Используем RAG для поиска релевантных чанков
#         relevant_chunks = find_relevant_chunks(prompt, top_n=5)
#         # Собираем контекст из найденных чанков
#         # Предполагается, что каждый результат имеет атрибут page_content
#         context_text = "\n".join([doc.page_content for doc in relevant_chunks])
#         # Формируем итоговый prompt, включающий контекст
#         full_prompt = f"Используя следующую информацию:\n{context_text}\nОтветь на вопрос: {prompt}"
#         print(full_prompt)
#         url = "http://localhost:11434/api/chat"
#         payload = {
#             "model": "owl/t-lite",  # Замените на используемое название модели, если необходимо
#             "messages": [{"role": "user", "content": prompt}]
#         }
#         try:
#             # Делаем запрос без streaming, чтобы дождаться полного ответа
#             api_response = requests.post(url, json=payload)
#             print(api_response.status_code)
#             print(api_response.text)
#             if api_response.status_code == 200:
#                 # Разбиваем полученный текст по строкам, фильтруем пустые и сразу собираем итоговый ответ
#                 response_text = "".join(
#                     json.loads(line)["message"]["content"]
#                     for line in api_response.text.strip().splitlines()
#                     if line.strip()
#                 )
#                 print("Итоговый ответ:", response_text)
#             else:
#                 response_text = f"Ошибка: {api_response.status_code}\n{api_response.text}"
#         except Exception as e:
#             response_text = f"Исключение: {str(e)}"
#     return render(request, "pvz_app/chat.html", {"response_text": response_text, "prompt": prompt})

# import requests
# import json
# from django.shortcuts import render
# from .rag.faiss_index import find_relevant_chunks

# def chat_view(request):
#     response_text = ""
#     prompt = ""
#     if request.method == "POST":
#         prompt = request.POST.get("prompt", "")
#         # Используем RAG для поиска релевантных чанков
#         relevant_chunks = find_relevant_chunks(prompt, top_n=5)
#         # Собираем контекст из найденных чанков
#         # Предполагается, что каждый результат имеет атрибут page_content
#         context_text = "\n".join([doc.page_content for doc in relevant_chunks])
#         # Формируем итоговый prompt, включающий контекст
#         full_prompt = f"Используя следующую информацию:\n{context_text}\nОтветь на вопрос: {prompt}"
#         print(full_prompt)
#         url = "http://localhost:11434/api/chat"
#         payload = {
#             "model": "owl/t-lite",  # При необходимости можно поменять модель
#             "messages": [{"role": "user", "content": full_prompt}]
#         }
#         try:
#             api_response = requests.post(url, json=payload, stream=True)
#             print(api_response)
#             if api_response.status_code == 200:
#                 for line in api_response.iter_lines(decode_unicode=True):
#                     if line:
#                         try:
#                             print(line)
#                             json_data = json.loads(line)
#                             if "message" in json_data and "content" in json_data["message"]:
#                                 response_text += json_data["message"]["content"]
#                                 print(response_text)
#                         except json.JSONDecodeError:
#                             response_text += f"\nОшибка парсинга: {line}"
#             else:
#                 response_text = f"Ошибка: {api_response.status_code}\n{api_response.text}"
#         except Exception as e:
#             response_text = f"Исключение: {str(e)}"
#     return render(request, "pvz_app/chat.html", {"response_text": response_text, "prompt": prompt})

import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from .rag.faiss_index import find_relevant_chunks

def chat_view(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        prompt = request.POST.get("prompt", "")
        # Получаем релевантные чанки и собираем контекст
        relevant_chunks = find_relevant_chunks(prompt, top_n=5)
        context_text = "\n".join([doc.page_content for doc in relevant_chunks])
        full_prompt = f"Используя следующую информацию:\n{context_text}\nОтветь на вопрос: {prompt}"

        print(full_prompt)

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
    elif request.method == "POST":
        # Резервный вариант для обычного POST
        prompt = request.POST.get("prompt", "")
        relevant_chunks = find_relevant_chunks(prompt, top_n=5)
        context_text = "\n".join([doc.page_content for doc in relevant_chunks])
        full_prompt = f"Используя следующую информацию:\n{context_text}\nОтветь на вопрос: {prompt}"
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
        return render(request, "pvz_app/chat.html", {"response_text": response_text, "prompt": prompt})
    else:
        return render(request, "pvz_app/chat.html")
