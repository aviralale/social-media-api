from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from social.models import Follower
from .serializers import UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        data = serializer.data

        # Determine if the authenticated user is following the profile user
        if request.user.is_authenticated:
            data["is_following"] = Follower.objects.filter(
                user=request.user, followed=instance
            ).exists()
        else:
            data["is_following"] = False

        return Response(data)
