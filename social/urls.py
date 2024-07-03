from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    ReplyViewSet,
    MediaViewSet,
    FollowerViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"replies", ReplyViewSet)
router.register(r"media", MediaViewSet)
router.register(r"followers", FollowerViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:pk>/like/", PostViewSet.as_view({"post": "like"}), name="post-like"
    ),
    path(
        "comments/<int:pk>/like/",
        CommentViewSet.as_view({"post": "like"}),
        name="comment-like",
    ),
    path(
        "replies/<int:pk>/like/",
        ReplyViewSet.as_view({"post": "like"}),
        name="reply-like",
    ),
    path(
        "users/<int:pk>/posts/",
        UserViewSet.as_view({"get": "posts"}),
        name="user-posts",
    ),
    path(
        "users/<int:pk>/followers/",
        UserViewSet.as_view({"get": "followers"}),
        name="user-followers",
    ),
    path(
        "users/<int:pk>/following/",
        UserViewSet.as_view({"get": "following"}),
        name="user-following",
    ),
    path(
        "posts/<int:pk>/comments/",
        PostViewSet.as_view({"get": "comments"}),
        name="post-comments",
    ),
    path(
        "posts/<int:pk>/likers/",
        PostViewSet.as_view({"get": "likers"}),
        name="post-likers",
    ),
    path(
        "comments/<int:pk>/replies/",
        CommentViewSet.as_view({"get": "replies"}),
        name="comment-replies",
    ),
    path(
        "comments/<int:pk>/likers/",
        CommentViewSet.as_view({"get": "likers"}),
        name="comment-likers",
    ),
    path(
        "replies/<int:pk>/likers/",
        ReplyViewSet.as_view({"get": "likers"}),
        name="reply-likers",
    ),
]
