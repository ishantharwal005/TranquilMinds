from django.urls import re_path
from apps.video.consumers import SignalingConsumer

websocket_urlpatterns = [
    re_path(r'^ws/signal/therapist_(?P<therapist_id>\d+)_client_(?P<client_id>\d+)/$', SignalingConsumer.as_asgi()),
]

