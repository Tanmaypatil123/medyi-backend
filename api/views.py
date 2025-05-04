from django.shortcuts import render

from api.authications.TokenGenerator import TokenGenerator
from api.authications.api_authentication import MyAuthentication
from api.models import CustomUser
from api.services import login_or_register_user, get_data_and_create_user_chat_model, generate_access_token_service, \
    get_discover_data, connect_ai_character_to_user, get_chat_list_screen_data, get_chat_room_data
from api.tasks import tryfun
from api.utils.base_view import BaseAPIView
from api.Llmserver.llm_utils import get_chat_response, get_system_prompt
from api.utils.response import status_200, handle_post_exception
import logging

logger = logging.getLogger(__name__)


# Create your views here.

class RegisterUser(BaseAPIView):

    @handle_post_exception
    def post(self, request):
        email = request.data.get("email", None)
        print("here is coming...............")
        data = login_or_register_user(email=email)
        return status_200(message="Register user Data.", data={"data": data})


class GetDataAndCreateUserChatModel(BaseAPIView):
    # authentication_classes = (MyAuthentication,)

    @handle_post_exception
    def post(self, request):
        user_id = CustomUser.objects.get(id=1).id #request.user.id
        data = get_data_and_create_user_chat_model(user_id=user_id,data=request.data)
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


class GetDiscoversData(BaseAPIView):
    authentication_classes = (MyAuthentication,)

    def post(self,request):
        user_id = request.user.id
        data = get_discover_data(user_id=user_id)
        return status_200(message="Discover Data",data=data)


class ConnectToAiCharacter(BaseAPIView):
    authentication_classes = (MyAuthentication,)

    def post(self,request):
        ai_character_ai = request.data.get("ai_character_ai",None)
        if not ai_character_ai:
            return status_200(message="connect ai", data={})
        data = connect_ai_character_to_user(user_id=request.user.id,ai_character_ai=ai_character_ai)
        return status_200(message="connect ai",data=data)


class Tryapi(BaseAPIView):

    def post(self,request):
        # ai_character_ai = request.data.get("ai_character_ai",None)
        # if not ai_character_ai:
        #     return status_200(message="connect ai", data={})
        # data = connect_ai_character_to_user(user_id=1,ai_character_ai=ai_character_ai)
        # return status_200(message="connect ai",data=data)
        system_prompt = get_system_prompt("hello")
        output = get_chat_response(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Hello, how are you?"},
            ])
        
        print("output is here",output)
        return status_200(message="connect ai",data=output)



class GetChatListView(BaseAPIView):
    authentication_classes = (MyAuthentication,)

    def post(self,request):
        user_id = request.user.id
        data = get_chat_list_screen_data(user_id=user_id)
        return status_200(message="", data=data)


class GetRoomchats(BaseAPIView):
    authentication_classes = (MyAuthentication,)

    def post(self,request):
        user_id = request.user.id
        room_id = request.data.get("room_id",None)
        if not room_id:
            return status_200(message="", data={})
        data = get_chat_room_data(user_id=user_id,room_id=room_id)
        return status_200(message="", data=data)