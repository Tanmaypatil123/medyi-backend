from datetime import timedelta
from typing import Dict

from api.authications.TokenGenerator import TokenGenerator
from api.models import CustomUser, UserAiCharacter, Room, Message, RefreshTokenModel
from api.utils import datetime


def get_or_create_user(*, email: str):
    return CustomUser.objects.get_or_create(email=email, is_deleted=False)


def create_user_ai_character(*, user_id: int, data: Dict):
    return UserAiCharacter.objects.create(user_id=user_id, properties=data)


def get_or_create_group(*, user_id, ai_character_id: int):
    return Room.objects.create(initiator_id=user_id, initiatee_id=ai_character_id)


def save_chat_message(room_id: int, sender_id: int, message_type: str, message_content: str, ):
    return Message.objects.create(
        chat_id=room_id,
        sender_id=sender_id,
        message_type=message_type,
        content=message_content, )


def create_refresh_token(user_id: int):
    refresh_token, refresh_expire = TokenGenerator.refresh_token()
    refresh_data = {
        "refresh_token": refresh_token,
        "expire_in": datetime.now() + timedelta(seconds=refresh_expire),
        "user_id": user_id,
    }
    refresh_token_model = RefreshTokenModel.objects.create(**refresh_data)
    return refresh_token_model.refresh_token
