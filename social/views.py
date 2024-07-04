from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import (
    Post,
    Comment,
    Reply,
    Media,
    PostLike,
    CommentLike,
    ReplyLike,
    Follower,
)
from .serializers import (
    PostSerializer,
    CommentSerializer,
    ReplySerializer,
    MediaSerializer,
    FollowerSerializer,
)
from account.serializers import UserSerializer
from account.models import User


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if created:
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
        like.delete()
        return Response({"message": "Post unliked"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def likers(self, request, pk=None):
        post = self.get_object()
        likers = User.objects.filter(postlike__post=post)
        serializer = UserSerializer(likers, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            return Response(
                {"message": "Comment liked"}, status=status.HTTP_201_CREATED
            )
        like.delete()
        return Response(
            {"message": "Comment unliked"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=["get"])
    def replies(self, request, pk=None):
        comment = self.get_object()
        replies = Reply.objects.filter(comment=comment)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def likers(self, request, pk=None):
        comment = self.get_object()
        likers = User.objects.filter(commentlike__comment=comment)
        serializer = UserSerializer(likers, many=True)
        return Response(serializer.data)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        reply = self.get_object()
        user = request.user
        like, created = ReplyLike.objects.get_or_create(reply=reply, user=user)
        if created:
            return Response({"message": "Reply liked"}, status=status.HTTP_201_CREATED)
        like.delete()
        return Response({"message": "Reply unliked"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def likers(self, request, pk=None):
        reply = self.get_object()
        likers = User.objects.filter(replylike__reply=reply)
        serializer = UserSerializer(likers, many=True)
        return Response(serializer.data)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def follow(self, request):
        followed_username = request.data.get("followed")
        followed = get_object_or_404(User, username=followed_username)
        follower, created = Follower.objects.get_or_create(
            user=request.user, followed=followed
        )
        if created:
            return Response(
                {"message": "Now following"}, status=status.HTTP_201_CREATED
            )
        return Response({"message": "Already following"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"])
    def unfollow(self, request, username=None):
        followed = get_object_or_404(User, username=username)
        follower = get_object_or_404(Follower, user=request.user, followed=followed)
        follower.delete()
        return Response({"message": "Unfollowed"}, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "username"

    @action(detail=True, methods=["get"])
    def posts(self, request, username=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def followers(self, request, username=None):
        user = self.get_object()
        followers = User.objects.filter(following__followed=user)
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, username=None):
        user = self.get_object()
        following = User.objects.filter(followers__user=user)
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)
