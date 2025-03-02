import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import admin_panel.routing
import django

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filtering_service.settings')

import django
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            admin_panel.routing.websocket_urlpatterns
        )
    )
})