from typing import Dict, Tuple, Optional

from api.authications.TokenGenerator import TokenGenerator
from api.consumers.chat_consumer import BASE_USER_GROUP
from api.models import RefreshTokenModel, MessageType
from api.selectors import get_or_create_user, create_user_ai_character, create_refresh_token, get_or_create_group, \
    save_chat_message
from django.conf import settings
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.Llmserver.llm_utils import *
import logging

from api.utils.constants import ChatEvents

logger = logging.getLogger(__name__)


def login_or_register_user(*, email: str) -> Dict:
    user, created = get_or_create_user(email=email)
    refresh_token = create_refresh_token(user_id=user.id)
    access_token, access_expire = create_access_token(
        user_id=user.id
    )
    data = {
        "is_new_user": created,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return data


def get_data_and_create_user_chat_model(*, data: Dict, user_id: int) -> Dict:
    ai_character = create_user_ai_character(user_id=user_id, data=data)
    print(f"======== {ai_character=}")
    # Use delay() instead of apply_async for simpler calls
    return create_ai_model_for_user_and_assign(user_id=user_id, ai_character_id=ai_character.id)


def create_ai_model_for_user_and_assign(user_id: int, ai_character_id: int):
    room = get_or_create_group(user_id=user_id, ai_character_id=ai_character_id)
    print(f"[DEBUG] :: here.... {room.id} {ai_character_id=}")
    # generate ai model content

    content = "Hey, Hi"
    message = save_chat_message(
        room_id=room.id,
        sender_id=None,
        message_content=content,
        message_type=MessageType.TEXT.name,
    )
    return send_to_chat_room(
        BASE_USER_GROUP.format(user_id=message.sender_id), {"message": content},
        ChatEvents.chatlist_on_read_receipt.value
    )


def send_to_chat_room(
        group: str, message_data: dict, event_type: str
):
    logger.info(
        f'{group=} {message_data=} {event_type=}'
    )
    return {
        "type": "send_event",
        "event_name": event_type,
        "event_data": message_data,
    }


def create_access_token(*, user_id: int) -> Tuple[str, str]:
    access_token, _ = TokenGenerator.access_token()
    # store auth_token in cache
    cache_key, cache_timeout = get_cache_key_and_timeout("OAUTH_TOKEN_CACHE", token=access_token)
    cache.set(cache_key, user_id, cache_timeout)
    return access_token, cache_timeout


def generate_access_token_service(
        *, grant_type: TokenGenerator.GrantType.REFRESH_TOKEN, data: dict
) -> Optional[dict]:
    access_token_data = {}
    keys = data.keys()
    if "refresh_token" in keys and data["refresh_token"]:
        try:
            refresh_token_model = RefreshTokenModel.objects.get(
                refresh_token=data["refresh_token"]
            )
            if not refresh_token_model:
                return None

            custom_user = refresh_token_model.user
            user_id = custom_user.id
            if custom_user.is_blocked or custom_user.is_deleted:
                logger.info(
                    "[AUTH 2] grant_type {} user id {} blocked".format(grant_type.name, user_id)
                )
                return None

        except RefreshTokenModel.DoesNotExist:
            return None

        access_token, access_expire = create_access_token(
            user_id=user_id,
        )
        access_token_data["access_token"] = access_token
        access_token_data["expire_in"] = access_expire
        return access_token_data
    return None


def get_cache_key_and_timeout(dict_identifier, **kwargs):
    cache_dict = settings.CACHE_NAMES[dict_identifier]
    cache_key = cache_dict["key"].format(**kwargs)
    if callable(cache_dict["timeout"]):
        cache_timeout = cache_dict["timeout"]()
    else:
        cache_timeout = cache_dict["timeout"]
    return cache_key, cache_timeout
