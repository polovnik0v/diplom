from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from pvz_app.views import chat_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Для GET-запросов на корневой URL используем шаблон чата
    path('', TemplateView.as_view(template_name="pvz_app/chat.html"), name="chat-home"),
    # Для AJAX POST-запросов используем существующую вьюху chat_view
    path('chat/', chat_view, name="chat-ajax"),
]
