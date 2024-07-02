from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.jwt")),
]
