from django.urls import path, include

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # TODO: SOCIAL AUTH
]
