# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("start/<str:username>/", views.StartChatView.as_view(), name="start_chat"),
    path("room/<int:room_id>/", views.ChatRoomView.as_view(), name="chat_room"),
    path("chats/", views.GetUserChatsView.as_view(), name="get_user_chats"),
    path(
        "room/<int:room_id>/typing/",
        views.TypingStatusView.as_view(),
        name="typing_status",
    ),
]
