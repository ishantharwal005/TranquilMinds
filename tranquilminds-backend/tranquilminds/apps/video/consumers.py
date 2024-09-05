
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

# Setting up logging
logger = logging.getLogger(__name__)

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        therapist_id = self.scope['url_route']['kwargs']['therapist_id']
        client_id = self.scope['url_route']['kwargs']['client_id']
        self.room_group_name = f'video_{therapist_id}_{client_id}'
        
        logger.info(f'Connecting to Room Group Name: {self.room_group_name}')

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f'Disconnecting from Room Group Name: {self.room_group_name}')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            logger.info(f'Received message type: {message_type} in Room Group Name: {self.room_group_name}')

            # Forward the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'forward_message',
                    'message': text_data_json
                }
            )
        except Exception as e:
            logger.error(f'Error in receive method: {str(e)}')

    # Forward message from room group to WebSocket
    async def forward_message(self, event):
        message = event['message']

        try:
            logger.info(f'Forwarding message in Room Group Name: {self.room_group_name}')
            # Send message to WebSocket
            await self.send(text_data=json.dumps(message))
        except Exception as e:
            logger.error(f'Error in forward_message method: {str(e)}')

