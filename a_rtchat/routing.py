from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chatroom/<chatroom_name>', ChatroomConsumer.as_asgi()),
    path('ws/online-status/', OnlineStatusConsumer.as_asgi()),
]
