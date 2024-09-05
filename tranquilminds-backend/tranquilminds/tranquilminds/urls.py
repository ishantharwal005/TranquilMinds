from django.urls import include, re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.message.routing as message_routing
import apps.video.routing as video_routing

# Combine websocket patterns from both apps
websocket_urlpatterns = message_routing.websocket_urlpatterns + video_routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

urlpatterns = [
    re_path(r'^api/v1/', include('apps.user.urls')),
    re_path(r'^api/v1/', include('apps.therapist.urls')),
    re_path(r'^api/v1/', include('apps.message.urls')),
    re_path(r'^api/v1/', include('apps.video.urls')),
]