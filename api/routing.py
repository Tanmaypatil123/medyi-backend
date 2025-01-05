from django.urls import path

from api.consumers.chat_consumer import AiChatConsumer

websocket_urlpatterns = [path("chat", AiChatConsumer.as_asgi())]
