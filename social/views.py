from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
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
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from account.models import User
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if created:
            like.save()
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response(
                {"message": "Post unliked"}, status=status.HTTP_204_NO_CONTENT
            )

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


class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            like.save()
            return Response(
                {"message": "Comment liked"}, status=status.HTTP_201_CREATED
            )
        else:
            like.delete()
            return Response(
                {"message": "Comment unliked"}, status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=True, methods=["get"])
    def replies(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        replies = comment.replies.all()
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        reply = self.get_object()
        user = request.user
        like, created = ReplyLike.objects.get_or_create(reply=reply, user=user)
        if created:
            return Response({"status": "reply liked"})
        else:
            like.delete()
            return Response({"status": "reply unliked"})

    @action(detail=True, methods=["get"])
    def likers(self, request, pk=None):
        reply = self.get_object()
        likers = User.objects.filter(replylike__reply=reply)
        serializer = UserSerializer(likers, many=True)
        return Response(serializer.data)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        followed_id = request.data.get("followed")
        followed = get_object_or_404(User, id=followed_id)
        follower, created = Follower.objects.get_or_create(
            user=request.user, followed=followed
        )
        if created:
            return Response({"status": "Now following"}, status=status.HTTP_201_CREATED)
        return Response({"status": "Already following."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        followed = get_object_or_404(User, id=pk)
        follower = get_object_or_404(Follower, user=request.user, followed=followed)
        follower.delete()
        return Response({"status": "Unfollowed"}, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = Follower.objects.filter(followed=user)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        user = self.get_object()
        following = Follower.objects.filter(user=user)
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)
