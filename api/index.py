import sys
import os

# Add the project directory to sys.path so Python can find the 'app' package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "clinic-ai-receptionist"))

from app.main import app as fastapi_app  # noqa: E402


# ---------------------------------------------------------------------------
# ASGI wrapper — fixes path routing for Vercel rewrites
# ---------------------------------------------------------------------------
# When Vercel rewrites /health -> api/index.py, the function's ASGI scope
# receives path "/api/index" (the file path), not "/health" (the original).
# Vercel sets the x-matched-path header to the original path. We read it
# and restore scope["path"] so FastAPI routes correctly.

class PathRewriteMiddleware:
    """ASGI middleware that restores the original request path from Vercel's
    x-matched-path header so FastAPI route matching works correctly."""

    def __init__(self, asgi_app):
        self.app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope.get("headers", []))
            matched_path = headers.get(b"x-matched-path", b"").decode()

            if matched_path:
                # matched_path is the original path, e.g. "/health"
                # Preserve query string if present
                qs = scope.get("query_string", b"").decode()
                scope["path"] = matched_path
                if qs:
                    scope["path"] = matched_path.split("?")[0]
                    scope["query_string"] = qs.encode()

        return await self.app(scope, receive, send)


app = PathRewriteMiddleware(fastapi_app)
