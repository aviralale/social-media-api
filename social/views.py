from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

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


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        files = self.request.FILES.getlist("media")
        for file in files:
            Media.objects.create(post=post, file=file)

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
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

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
    queryset = Reply.objects.all().order_by("-created_at")
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPagination

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


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DynamicPageSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class HomePagePostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DynamicPageSizePagination

    def get_queryset(self):
        user = self.request.user
        following_users = Follower.objects.filter(user=user).values_list(
            "followed", flat=True
        )
        return Post.objects.filter(
            Q(author__in=following_users) | Q(author=user)
        ).order_by("-created_at")


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
    pagination_class = CustomPagination

    @action(detail=True, methods=["get"])
    def posts(self, request, username=None):
        user = self.get_object()
        posts = Post.objects.filter(author=user).order_by("-created_at")
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def post(self, request, username=None, pk=None):
        user = self.get_object()
        try:
            post = Post.objects.get(author=user, pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["get"])
    def followers(self, request, username=None):
        user = self.get_object()
        followers = User.objects.filter(following__followed=user).order_by(
            "-following__created_at"
        )
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, username=None):
        user = self.get_object()
        following = User.objects.filter(followers__user=user).order_by(
            "-followers__created_at"
        )
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def mutual_connections(self, request, username=None):
        user = self.get_object()
        current_user = request.user

        # Get users that the current user follows
        current_user_following = Follower.objects.filter(user=current_user).values_list(
            "followed", flat=True
        )

        mutual_connections = User.objects.filter(id__in=current_user_following)

        serializer = UserSerializer(mutual_connections, many=True)
        return Response(serializer.data)


class SuggestedUsersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following = Follower.objects.filter(user=user).values_list(
            "followed", flat=True
        )

        if not following:
            suggested_users = (
                User.objects.exclude(id=user.id)
                .annotate(mutuals=Count("followers"))
                .order_by("-mutuals")[:10]
            )
        else:
            suggested_users = (
                User.objects.exclude(id__in=following)
                .exclude(id=user.id)
                .annotate(mutuals=Count("followers", filter=Q(followers__user=user)))
                .order_by("-mutuals")[:10]
            )

        return suggested_users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExplorePostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DynamicPageSizePagination

    def get_queryset(self):
        user = self.request.user
        following_users = Follower.objects.filter(user=user).values_list(
            "followed", flat=True
        )

        # Get posts from users that the current user is not following
        explore_posts = (
            Post.objects.exclude(author__in=following_users)
            .exclude(author=user)
            .order_by("-created_at")
        )

        return explore_posts


class SearchViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        if not query:
            return Response({"results": []})

        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        )[:10]

        posts = Post.objects.filter(
            Q(content__icontains=query) | Q(author__username__icontains=query)
        )[:20]

        user_serializer = UserSerializer(users, many=True)
        post_serializer = PostSerializer(posts, many=True)

        results = {
            "profiles": user_serializer.data,
            "posts": post_serializer.data,
        }

        return Response(results)
