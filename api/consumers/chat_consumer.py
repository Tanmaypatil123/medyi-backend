from channels.generic.websocket import AsyncJsonWebsocketConsumer

import logging

from api.consumers.cusumer_utils import sample_reponse
from api.services import send_and_save_message_in_chat

logger = logging.getLogger(__name__)

BASE_USER_GROUP = f"AI_"


class AiChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.user_id = self.scope['user']
        except:
            await self.close()
            return
        await self.accept()
        print(f'[Connect] {self.scope=} {self.user_id}')
        await self.channel_layer.group_add(BASE_USER_GROUP.format(user_id=self.user_id), self.channel_name)
        await self.send_json({"message":"user connected to socket"})

    async def disconnect(self, close_code):

        logger.info(f'[ Disconnect User ] {self.user_id=} {close_code=} {self.channel_name}')
        await self.channel_layer.group_discard(BASE_USER_GROUP.format(user_id=self.user_id), self.channel_name)
        '''
        here update last connected for the user
        '''

    async def event_mapping(self):
        event_mapping = {
            "send_message": self.send_message,

        }
        return event_mapping

    async def receive_json(self, event, **kwargs):
        event_type = event["type"]
        print(event_type)
        events = await self.event_mapping()
        event_function = events[event_type]
        logger.info(
            f'{event=}'
        )
        await event_function(event["data"])

    async def send_message(self, data):
        ai_character_id = data.get("ai_bot_id",None)
        message = data.get("message","")
        if not ai_character_id:
            await self.send_json(sample_reponse(data["event_name"], data={"message": "invalid ai"}))
            return

        await send_and_save_message_in_chat(user_id=self.user_id,ai_character_id=ai_character_id,message_content=message)

    async def send_event(self, data):
        logger.info(
            f'{data=}'
        )
        await self.send_json(sample_reponse(data["event_name"], data=data["event_data"]))

