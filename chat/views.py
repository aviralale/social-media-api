# chat/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatRoom, Message, TypingStatus
from social.models import Follower
from account.models import User


class StartChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        other_user = get_object_or_404(User, username=username)
        is_following = Follower.objects.filter(
            user=request.user, followed=other_user
        ).exists()
        is_followed = Follower.objects.filter(
            user=other_user, followed=request.user
        ).exists()

        if is_following and is_followed:
            chatroom = ChatRoom.get_or_create_chatroom(request.user, other_user)
            return Response({"room_id": chatroom.id}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "You can only chat with users who follow each other."},
                status=status.HTTP_403_FORBIDDEN,
            )


class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        if request.user not in chatroom.participants.all():
            return Response(
                {"message": "You are not a participant in this chat room."},
                status=status.HTTP_403_FORBIDDEN,
            )
        messages = chatroom.messages.all().order_by("timestamp")

        # Mark messages as seen
        messages.exclude(sender=request.user).update(is_seen=True)

        # Get typing status
        other_user = chatroom.participants.exclude(id=request.user.id).first()
        typing_status = TypingStatus.objects.filter(
            chatroom=chatroom, user=other_user
        ).first()
        is_typing = typing_status.is_typing if typing_status else False

        serialized_messages = [
            {
                "id": msg.id,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "sender": msg.sender.username,
                "is_delivered": msg.is_delivered,
                "is_seen": msg.is_seen,
            }
            for msg in messages
        ]
        return Response(
            {
                "chatroom_id": chatroom.id,
                "messages": serialized_messages,
                "other_user_typing": is_typing,
                "other_user": {
                    "id": other_user.id,
                    "username": other_user.username,
                    "profile_pic": other_user.profile_pic.url,
                },
            }
        )

    def post(self, request, room_id):
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        if request.user not in chatroom.participants.all():
            return Response(
                {"message": "You are not a participant in this chat room."},
                status=status.HTTP_403_FORBIDDEN,
            )
        content = request.data.get("content")
        if not content:
            return Response(
                {"message": "Message content is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        message = Message.objects.create(
            chatroom=chatroom,
            sender=request.user,
            content=content,
            is_delivered=True,  # Assuming immediate delivery in this example
        )
        return Response(
            {
                "id": message.id,
                "content": message.content,
                "timestamp": message.timestamp,
                "sender": message.sender.username,
                "is_delivered": message.is_delivered,
                "is_seen": message.is_seen,
            },
            status=status.HTTP_201_CREATED,
        )


class GetUserChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_chatrooms = ChatRoom.objects.filter(participants=request.user)
        chats_data = []
        for chatroom in user_chatrooms:
            other_user = chatroom.participants.exclude(id=request.user.id).first()
            last_message = chatroom.messages.order_by("-timestamp").first()

            # Get typing status
            typing_status = TypingStatus.objects.filter(
                chatroom=chatroom, user=other_user
            ).first()
            is_typing = typing_status.is_typing if typing_status else False

            chat_data = {
                "id": chatroom.id,
                "other_user": {
                    "id": other_user.id,
                    "username": other_user.username,
                    "profile_pic": other_user.profile_pic.url,
                },
                "last_message": {
                    "content": last_message.content if last_message else None,
                    "timestamp": last_message.timestamp if last_message else None,
                    "sender": (
                        {
                            "id": last_message.sender.id if last_message else None,
                            "username": (
                                last_message.sender.username if last_message else None
                            ),
                        }
                        if last_message
                        else None
                    ),
                    "is_delivered": last_message.is_delivered if last_message else None,
                    "is_seen": last_message.is_seen if last_message else None,
                },
                "other_user_typing": is_typing,
            }
            chats_data.append(chat_data)
        return Response(chats_data)


class TypingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        if request.user not in chatroom.participants.all():
            return Response(
                {"message": "You are not a participant in this chat room."},
                status=status.HTTP_403_FORBIDDEN,
            )
        is_typing = request.data.get("is_typing", False)
        TypingStatus.objects.update_or_create(
            chatroom=chatroom, user=request.user, defaults={"is_typing": is_typing}
        )
        return Response({"status": "updated"}, status=status.HTTP_200_OK)
