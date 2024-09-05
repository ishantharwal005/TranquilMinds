
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import connection

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f'chat_{self.scope["url_route"]["kwargs"]["therapist_id"]}_{self.scope["url_route"]["kwargs"]["user_id"]}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Added to group: {self.room_group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Removed from group: {self.room_group_name}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json.get('sender')
        recipient_id = text_data_json.get('recipient')

        #Save the message to the database
        await self.save_message(sender_id, recipient_id, message)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print(f"Message sent to group: {self.room_group_name}")

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
        print(f"Message received in group: {self.room_group_name}")

    @database_sync_to_async
    def save_message(self, sender, recipient, content):
        # with connection.cursor() as cursor:
        #     cursor.execute("INSERT INTO message (sender, recipient, content) VALUES (%s, %s, %s)", [sender, recipient, content])
        from apps.message.models import Message
        Message.objects.create(senderid=sender, recipientid=recipient, content=content)
