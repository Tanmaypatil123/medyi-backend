from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.core.cache import  cache

from api.models import CustomUser

AUTH_ERROR = exceptions.NotAuthenticated("Invalid Request")
AUTHENTICATION_HEADER = "HTTP_AUTHORIZATION"
APPVERSION_HEADER = "HTTP_APPVERSION"
import logging
logger = logging.getLogger(__name__)

class MyAuthentication(BaseAuthentication):
    def authenticate_header(self, request):
        return "Failed"

    def check_auth_token(self, auth_token):
        if auth_token is None:
            raise AUTH_ERROR
        user = CustomUser.objects.filter(auth_token=auth_token).first()
        if not user:
            user = CustomUser.objects.using("write").filter(auth_token=auth_token).first()
        if not user:
            raise AUTH_ERROR
        return user, None

    def handle_access_token(self, access_token: str, app_version: int):
        user_id = cache.get(access_token)
        if user_id is None or user_id == -1:
            raise AUTH_ERROR
        user = CustomUser.objects.using("write").filter(id=user_id).first()
        if not user:
            user = CustomUser.objects.using("write").filter(id=user_id).first()
        if not user:
            raise AUTH_ERROR
        if user.is_blocked:
            raise AUTH_ERROR
        return user, None

    def authenticate(self, request):
        auth_token = request.META.get(AUTHENTICATION_HEADER, None)
        app_version = int(request.META.get(APPVERSION_HEADER, 0))
        if not auth_token:
            raise exceptions.NotAuthenticated("Invalid Request")

        if "OAuth" in auth_token:
            try:
                access_token = auth_token.split(" ")[1]
            except IndexError:
                raise AUTH_ERROR
            return self.handle_access_token(
                "OAuth_{}".format(access_token), app_version=app_version
            )
        else:
            return self.check_auth_token(auth_token)
