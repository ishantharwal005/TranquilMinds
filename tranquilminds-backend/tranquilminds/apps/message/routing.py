from django.urls import re_path

from apps.message.consumers import ChatConsumer


websocket_urlpatterns = [
     re_path(r'^ws/chat/chat_(?P<therapist_id>\d+)_(?P<user_id>\d+)/$', ChatConsumer.as_asgi()),
]
