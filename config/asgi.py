"""Unified ASGI application routing requests to FastAPI (Partner API /docs)

and Django (Admin Panel).
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django_application = get_asgi_application()

# Import FastAPI application
from api.main import app as fastapi_application


async def application(scope, receive, send):
    """Route API and documentation paths to FastAPI, all other paths to Django."""
    if scope["type"] in ("http", "websocket"):
        path = scope.get("path", "")
        if (
            path.startswith("/v1")
            or path.startswith("/docs")
            or path.startswith("/openapi.json")
            or path.startswith("/redoc")
            or path.startswith("/health")
        ):
            await fastapi_application(scope, receive, send)
            return
    await django_application(scope, receive, send)
