from django.shortcuts import render

from api.authications.TokenGenerator import TokenGenerator
from api.services import login_or_register_user, get_data_and_create_user_chat_model, generate_access_token_service
from api.utils.base_view import BaseAPIView
from api.utils.response import status_200
import logging

logger = logging.getLogger(__name__)


# Create your views here.

class RegisterUser(BaseAPIView):
    def post(self, request):
        email = request.data.get("email", None)

        data = login_or_register_user(email=email)
        return status_200(message="Register user Data.", data={"data": data})


class GetDataAndCreateUserChatModel(BaseAPIView):
    def post(self, request):
        data = get_data_and_create_user_chat_model(data=request.data)
        return status_200(message="Created Chat Model", data=data)


class GetAccessTokenApi(BaseAPIView):
    def post(self, request):
        token_data = request.data.copy()
        token_data = generate_access_token_service(
            grant_type=TokenGenerator.GrantType.REFRESH_TOKEN,
            data=token_data,
        )
        if token_data:
            logger.info("[AUTH 2] data {} refresh_token".format(token_data))
            return status_200("access token generated", data=token_data)
        else:
            logger.info("[AUTH 2] refresh_token_expired")
            return status_200("refresh token expired")
