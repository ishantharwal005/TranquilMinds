import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.message.routing as message_routing
import apps.video.routing as video_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tranquilminds.settings')

django.setup()

# Combine websocket patterns from both apps
websocket_urlpatterns = message_routing.websocket_urlpatterns + video_routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Django's ASGI application to handle traditional HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Use combined websocket routes
        )
    ),
})