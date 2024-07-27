from django.urls import path
from . import views

urlpatterns = [
    path(
        "notifications/", views.NotificationListView.as_view(), name="notification-list"
    ),
    path(
        "notifications/<int:pk>/",
        views.NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    path(
        "notifications/mark-all-as-read/",
        views.MarkAllAsReadView.as_view(),
        name="mark-all-as-read",
    ),
]
