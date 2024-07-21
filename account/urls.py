from django.urls import path, include
from .views import UserDetailView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("user/<str:username>/", UserDetailView.as_view(), name="user-detail"),
    # TODO: SOCIAL AUTH
]
