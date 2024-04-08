import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpRequest
from .models import Message
from authentication.models import User
from rest_framework.request import Request
from .views import chat_endpoint
from asgiref.sync import sync_to_async
from django.db.models import F
from django.db.models.functions import TruncDate
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connecting to WebSocket...")
        self.room_name = "_".join(sorted([self.scope['url_route']['kwargs']['sender_id'], self.scope['url_route']['kwargs']['recipient_id']]))
        self.room_group_name = f'chat_{self.room_name}'
        
        print(f'Connecting to room group: {self.room_group_name}')

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        sender_id = self.scope['url_route']['kwargs']['sender_id']
        receiver_id = self.scope['url_route']['kwargs']['recipient_id']
        
        # Fetch sender and receiver asynchronously
        # Fetch sender and receiver asynchronously
        sender = await self.get_user(sender_id)
        receiver = await self.get_user(receiver_id)
        
        # Fetch previous messages from the database asynchronously
        previous_messages_our = await self.get_previous_messages(sender, receiver)
        previous_messages_your = await self.get_previous_messages(receiver, sender)
       
        await self.accept()
        print(f'WebSocket Connected: {self.room_group_name}')
        # Prepare and send previous messages from ourselves to the client

        # Convert previous messages to lists
        previous_messages_our = await sync_to_async(list)(previous_messages_our)
        previous_messages_your = await sync_to_async(list)(previous_messages_your)
        
        for message in previous_messages_our:
            
            await self.send(text_data=json.dumps({
                'message': "previous_message",
                'messageInput': message['body'],
                'timestamp' : message['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                'sender': 'me',
            }))
        
        # Prepare and send previous messages from the other participant to the client
        for message in previous_messages_your:
            await self.send(text_data=json.dumps({
                'message': "previous_message",
                'messageInput': message['body'],
                'timestamp' : message['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                'sender': 'you',
            }))
            
    async def get_user(self, user_id):
        return await sync_to_async(User.objects.get)(id=user_id)
    
    async def get_previous_messages(self, sender, receiver):
        return await sync_to_async(list)(Message.objects.filter(sender=sender, recipient=receiver).values())

    async def disconnect(self, close_code):
        print(f'WebSocket Disconnected: {self.channel_name}, close_code: {close_code}')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Received message from WebSocket:")
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']

        # Save message to database
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)
        
        message = await sync_to_async(Message.objects.create)(
            sender=sender,
            recipient=receiver,
            body=text_data_json['message'],
            timestamp = datetime.now(),
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': "success",
                'messageInput' : message.body,
                'timestamp' : message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'msgsender': message.sender.id,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print("Received message from room group:")
        print(event)
        message = event['message']
        messageInput = event['messageInput']
        timestamp = event['timestamp']
        msgsender = event['msgsender']
        
        print("Message: ", msgsender)
        
        senderid = self.scope['url_route']['kwargs']['sender_id']
        
        print("Sender: ", senderid)
        
        # Convert msgsender to a string before comparison
        chat_sender = 'me' if str(msgsender) == senderid else 'you'

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'messageInput': messageInput,
            'timestamp': timestamp,
            'sender': chat_sender,
        }))
