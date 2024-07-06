from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "password", "first_name", "last_name")


class UserSerializer(BaseUserSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "profile_pic",
            "cover_pic",
            "bio",
            "gender",
            "follower_count",
            "following_count",
            "is_verified",
            "date_of_birth",
            "is_active",
            "is_admin",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
            "post_count",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_admin",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
        ]

    def get_follower_count(self, obj):
        return obj.follower_count()

    def get_following_count(self, obj):
        return obj.following_count()

    def get_full_name(self, obj):
        return obj.get_full_name()
