from django.shortcuts import render

from api.services import login_or_register_user, get_data_and_create_user_chat_model
from api.utils.base_view import BaseAPIView
from api.utils.response import status_200


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
