from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification(recipient, sender, notification_type, post=None):
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        post=post,
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}_notifications",
        {
            "type": "send_notification",
            "message": {
                "id": notification.id,
                "notification_type": notification_type,
                "sender": {
                    "username": sender.username,
                    "profile_pic": (
                        sender.profile_pic.url if sender.profile_pic else None
                    ),
                },
                "post": post.id,
                "created_at": notification.created_at.isoformat(),
            },
        },
    )
