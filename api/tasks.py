from celery import shared_task
from channels.layers import get_channel_layer
from api.consumers.chat_consumer import BASE_USER_GROUP
from api.models import MessageType
from api.selectors import get_or_create_group, save_chat_message
from api.utils.constants import ChatEvents
from asgiref.sync import async_to_sync

import logging

logger = logging.getLogger(__name__)


@shared_task
def create_ai_model_for_user_and_assign(user_id: int, ai_character_id: int):
    room, created = get_or_create_group(user_id, ai_character_id=ai_character_id)
    # generate ai model content
    content = "somerhing"
    message = save_chat_message(
        room_id=room.id,
        sender_id=ai_character_id,
        message_content=content,
        message_type=MessageType.TEXT.name,
    )
    send_event_to_chat_room_by_group.apply_async(
        [BASE_USER_GROUP.format(user_id=message.sender_id), {"message": content},
         ChatEvents.chatlist_on_read_receipt.value]
    )


@shared_task
def send_event_to_chat_room_by_group(
        group: str, message_data: dict, event_type: str
):
    logger.info(
        f'{group=} {message_data=} {event_type=}'
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type": "send_event",
            "event_name": event_type,
            "event_data": message_data,
        },
    )
