# Standard Library
import logging
from django.core.cache import cache


from asgiref.sync import sync_to_async

from api.models import CustomUser
from api.utils.constants import AUTH_ERROR

logger = logging.getLogger(__name__)


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 3
    """

    def __init__(self, inner):
        self.inner = inner

    def handle_access_token(self, access_token: str, app_version: int) -> int:
        user_id = cache.get(access_token)
        if user_id is None or user_id == -1:
            raise AUTH_ERROR
        user = CustomUser.objects.get(id=user_id)
        if user.is_blocked:
            raise AUTH_ERROR

        return user_id

    async def __call__(self, scope, receive, send):
        print("inside auth")
        headers = dict(scope["headers"])
        scope["user"] = None

        try:
            token = headers[b"authorization"].decode("utf-8")
            # app_version = headers.get(b"app-version", 0).decode("utf-8")
            # todo: remove it after testing
            app_version = 101
            if token is not None:
                user_id = await sync_to_async(self.handle_access_token)(
                    f"OAuth_{token}", app_version=int(app_version)
                )
                if user_id is not None:
                    scope["user"] = user_id
                    scope["app_version"] = int(app_version)
            scope["device"] = (
                headers.get(b"deviceid").decode("utf-8") if headers.get(b"deviceid") else ""
            )
            scope["device_info"] = (
                headers.get(b"deviceinfo").decode("utf-8") if headers.get(b"deviceinfo") else ""
            )
            scope["ip"] = (
                headers.get(b"x-real-ip").decode("utf-8") if headers.get(b"x-real-ip") else ""
            )
        except Exception as e:
            logger.info(f"{e}", exc_info=True)
        return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))  # noqa
