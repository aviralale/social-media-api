import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from account.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Get the token from the query string
            token = self.scope["query_string"].decode().split("=")[1]
            # Validate the token and get the user
            user = await self.get_user_from_token(token)

            if user:
                self.user = user
                self.room_group_name = f"user_{self.user.id}_notifications"
                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )
                await self.accept()
            else:
                await self.close()
        except (IndexError, InvalidToken, TokenError):
            # If token is invalid or not provided, close the connection
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # Validate the token
            validated_token = AccessToken(token)
            user_id = validated_token["user_id"]

            # Get the user
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist):
            return None
