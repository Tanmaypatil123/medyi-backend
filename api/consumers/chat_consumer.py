from channels.generic.websocket import AsyncJsonWebsocketConsumer

import logging

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
        logger.info(f'[Connect] {self.scope=} {self.user_id}')
        await self.channel_layer.group_add(BASE_USER_GROUP.format(user_id=self.user_id), self.channel_name)

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
        events = await self.event_mapping()
        event_function = events[event_type]
        logger.info(
            f'{event=}'
        )
        await event_function(event["data"])

    async def send_message(self, data):
        pass
