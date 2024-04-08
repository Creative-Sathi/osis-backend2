# chat/urls.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<sender_id>\d+)/(?P<recipient_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
