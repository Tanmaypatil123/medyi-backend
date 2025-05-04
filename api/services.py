import random
from typing import Dict, Tuple, Optional

from api.authications.TokenGenerator import TokenGenerator
from api.consumers.chat_consumer import BASE_USER_GROUP
from api.models import RefreshTokenModel, MessageType, AICharacterType, UserAiCharacter
from api.selectors import (
    get_or_create_user, create_user_ai_character, create_refresh_token, get_or_create_group,
    save_chat_message, get_all_ai_characters, get_or_create_user_ai_character, get_user_chat_room,
    get_chat_room_maessages
)
from django.conf import settings
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.Llmserver.llm_utils import *
import logging

from api.utils.constants import ChatEvents, FEMAL_AI_BOT_URL

logger = logging.getLogger(__name__)


def login_or_register_user(*, email: str) -> Dict:
    user, created = get_or_create_user(email=email)
    refresh_token = create_refresh_token(user_id=user.id)
    access_token, access_expire = create_access_token(user_id=user.id)
    return {
        "is_new_user": created,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def get_data_and_create_user_chat_model(*, data: Dict, user_id: int) -> Dict:
    ai_bot_image = random.choice(FEMAL_AI_BOT_URL)
    ai_bot_name = data.get("name","")
    ai_character = create_user_ai_character(user_id=user_id, data=data,ai_bot_image=ai_bot_image,ai_bot_name=ai_bot_name)
    print(f"======== {ai_character=}")
    return create_ai_model_for_user_and_assign(user_id=user_id, ai_character_id=ai_character.id)


def create_ai_model_for_user_and_assign(user_id: int, ai_character_id: int):
    room = get_or_create_group(user_id=user_id, ai_character_id=ai_character_id)
    print(f"[DEBUG] :: here.... {room.id} {ai_character_id=}")
    # generate ai model content

    # content = "Hey, Hi"
    system_prompt = get_system_prompt("hello")
    output = get_chat_response(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Hello, how are you?"},
        ])
    message = save_chat_message(
        room_id=room.id,
        sender_id=None,
        message_content=output,
        message_type=MessageType.TEXT.name,
    )
    return api_send_to_chat_room(
        BASE_USER_GROUP.format(user_id=message.sender_id), {"message": output},
        ChatEvents.received_message.value
    )


def send_and_save_message_in_chat(*,user_id: int, ai_character_id: int, message_content: str):
    print(f"[DEBUG] ::  here is coming .. {user_id=}, {ai_character_id=}")
    room = get_or_create_group(user_id=user_id, ai_character_id=ai_character_id)
    print(f"[DEBUG] :: here.... {room.id} {ai_character_id=}")
    system_prompt = get_system_prompt("hello")
    # todo: samadhan here need to ask @tanmay how to handle
    output = get_chat_response(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Hello, how are you?"},
        ])
    user_message = save_chat_message(
        room_id=room.id,
        sender_id=user_id,
        message_content=message_content,
        message_type=MessageType.TEXT.name,
    )
    ai_bot_chat = save_chat_message(
        room_id=room.id,
        sender_id=None,
        message_content=output,
        message_type=MessageType.TEXT.name,
    )
    return send_to_chat_room(
        BASE_USER_GROUP.format(user_id=user_id), {"message": output},
        ChatEvents.received_message.value
    )


def send_to_chat_room(group: str, message_data: dict, event_type: str):
    logger.info(f'{group=} {message_data=} {event_type=}')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type": "send_event",
            "event_name": event_type,
            "event_data": message_data,
        },
    )


def api_send_to_chat_room(group: str, message_data: dict, event_type: str):
    logger.info(f'{group=} {message_data=} {event_type=}')
    return {
        "type": "send_event",
        "event_name": event_type,
        "event_data": message_data,
    }


def create_access_token(*, user_id: int) -> Tuple[str, str]:
    access_token, _ = TokenGenerator.access_token()
    cache_key, cache_timeout = get_cache_key_and_timeout("OAUTH_TOKEN_CACHE", token=access_token)
    cache.set(cache_key, user_id, cache_timeout)
    return access_token, cache_timeout


def generate_access_token_service(
        *, grant_type: TokenGenerator.GrantType.REFRESH_TOKEN, data: dict
) -> Optional[dict]:
    if "refresh_token" not in data or not data["refresh_token"]:
        return None

    try:
        refresh_token_model = RefreshTokenModel.objects.get(refresh_token=data["refresh_token"])
        if not refresh_token_model:
            return None

        custom_user = refresh_token_model.user
        user_id = custom_user.id
        if custom_user.is_blocked or custom_user.is_deleted:
            logger.info(f"[AUTH 2] grant_type {grant_type.name} user id {user_id} blocked")
            return None

    except RefreshTokenModel.DoesNotExist:
        return None

    access_token, access_expire = create_access_token(user_id=user_id)
    return {
        "access_token": access_token,
        "expire_in": access_expire
    }


def get_cache_key_and_timeout(dict_identifier, **kwargs):
    cache_dict = settings.CACHE_NAMES[dict_identifier]
    cache_key = cache_dict["key"].format(**kwargs)
    cache_timeout = cache_dict["timeout"]() if callable(cache_dict["timeout"]) else cache_dict["timeout"]
    return cache_key, cache_timeout


def get_discover_data(*, user_id: int) -> Dict:
    ai_characters = get_all_ai_characters()
    data = {
        "public": [],
        "exclusive": [],
    }
    for ai_character in ai_characters:
        character_data = {
            "id": ai_character.id,
            "name": ai_character.name,
            "bio": ai_character.bio,
            "image_url": ai_character.image_url,
            "characterType": ai_character.characterType,
            "tags": ai_character.properties("tags", [])
        }
        if ai_character.characterType == AICharacterType.EXCLUSIVE.name:
            data["exclusive"].append(character_data)
        else:
            data["public"].append(character_data)
    return data


def connect_ai_character_to_user(*, user_id: int, ai_character_ai: int):
    ai_character, created = get_or_create_user_ai_character(user_id=user_id, ai_character_ai=ai_character_ai)
    if created:
        ai_character.properties = ai_character.properties.get("ai_properties", None)
        ai_character.save()
    return create_ai_model_for_user_and_assign(user_id=user_id, ai_character_id=ai_character.id)


def get_chat_list_screen_data(*, user_id: int) -> Dict:
    chat_rooms = get_user_chat_room(user_id=user_id)
    return [
        {
            "room_id": room.id,
            "name": room.initiatee.name,
            "profile_url": room.initiatee.image_url,
            "last_message_at": room.last_message_at,
            "message": room.message.content if room.message else ""
        }
        for room in chat_rooms
    ]


def get_chat_room_data(*, user_id: int, room_id: int) -> Dict:
    chat_room_messages = get_chat_room_maessages(user_id=user_id, room_id=room_id)
    initiatee = chat_room_messages.first().room.initiatee
    return {
        "room_chat": [
            {
                "message": room_chat.content,
                "sender": room_chat.sender_id,
                "created_at": room_chat.created_at
            }
            for room_chat in chat_room_messages
        ],
        "profile_data": {
            "name": initiatee.name,
            "profile_url": initiatee.image_url,
            "is_online": True
        }
    }
