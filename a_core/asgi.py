"""
ASGI config for a_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

django_asgi_app = get_asgi_application()

from a_rtchat import routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    # Эта цепочка middlewares обрабатывает ВСЕ WebSocket-подключения:
    # 1. AllowedHostsOriginValidator — разрешает только подключения с доверенных сайтов (по ALLOWED_HOSTS).
    # 2. AuthMiddlewareStack — добавляет в соединение пользователя и сессию Django (self.scope["user"]).
    # 3. URLRouter — по адресу определяет, какой consumer будет обслуживать соединение.
    # Благодаря этому WebSocket-запросы защищены, поддерживают авторизацию и маршрутизируются правильно.
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
    ),
})
