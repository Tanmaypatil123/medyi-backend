"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from api.authications.WebSocketAuthentication import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_app.settings")

application = get_asgi_application()


import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_app.settings.base")
django_asgi_app = get_asgi_application()

import api.routing


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleware(URLRouter(api.routing.websocket_urlpatterns)),
    }
)