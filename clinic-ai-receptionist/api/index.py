import os

from app.main import app as fastapi_app


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
                qs = scope.get("query_string", b"").decode()
                scope["path"] = matched_path
                if qs:
                    scope["path"] = matched_path.split("?")[0]
                    scope["query_string"] = qs.encode()

        return await self.app(scope, receive, send)


app = PathRewriteMiddleware(fastapi_app)
