from rest_framework import serializers
from .models import (
    Post,
    Comment,
    Reply,
    Media,
    Follower,
    PostLike,
    CommentLike,
    ReplyLike,
)
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "follower_count",
            "following_count",
            "is_verified",
            "profile_pic",
        ]

    def get_follower_count(self, obj):
        return obj.follower_count()

    def get_following_count(self, obj):
        return obj.following_count()


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "post", "file"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "media",
            "created_at",
            "like_count",
            "comment_count",
        ]

    def get_like_count(self, obj):
        return obj.like_count()

    def get_comment_count(self, obj):
        return obj.comment_count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "post",
            "content",
            "created_at",
            "like_count",
            "reply_count",
        ]

    def get_like_count(self, obj):
        return obj.like_count()

    def get_reply_count(self, obj):
        return obj.reply_count()


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ["id", "author", "comment", "content", "created_at", "like_count"]

    def get_like_count(self, obj):
        return obj.like_count()


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ["id", "post", "user", "created_at"]


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ["id", "comment", "user", "created_at"]


class ReplyLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ReplyLike
        fields = ["id", "reply", "user", "created_at"]


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "user", "followed", "created_at"]
