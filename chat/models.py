# chat/models.py
from django.db import models
from account.models import User


class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name="chatrooms")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_or_create_chatroom(cls, user1, user2):
        chatroom = (
            cls.objects.filter(participants=user1).filter(participants=user2).first()
        )
        if not chatroom:
            chatroom = cls.objects.create()
            chatroom.participants.add(user1, user2)
        return chatroom


class Message(models.Model):
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)


class TypingStatus(models.Model):
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="typing_statuses"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_typing = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
