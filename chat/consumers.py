import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, TypingStatus
from django.core.exceptions import ObjectDoesNotExist
from account.models import User
import jwt
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope["query_string"].decode().split("token=")[-1]
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.scope["user"] = await self.get_user(decoded_data["user_id"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
            await self.close()
            return

        if not self.scope["user"]:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")
        is_typing = text_data_json.get("is_typing", False)

        if is_typing is not None:
            await self.update_typing_status(is_typing)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "is_typing": is_typing,
                "sender": self.scope["user"].username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        is_typing = event["is_typing"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps(
                {"message": message, "is_typing": is_typing, "sender": sender}
            )
        )

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def update_typing_status(self, is_typing):
        try:
            chatroom = ChatRoom.objects.get(id=self.room_id)
            TypingStatus.objects.update_or_create(
                chatroom=chatroom,
                user=self.scope["user"],
                defaults={"is_typing": is_typing},
            )
        except ObjectDoesNotExist:
            pass
