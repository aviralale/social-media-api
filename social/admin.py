from django.contrib import admin
from .models import (
    Post,
    Media,
    Comment,
    Reply,
    PostLike,
    CommentLike,
    ReplyLike,
    Follower,
)


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at", "media_count")
    inlines = [MediaInline]

    def media_count(self, obj):
        return obj.media.count()

    media_count.short_description = "Media Count"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "content", "created_at")


class ReplyAdmin(admin.ModelAdmin):
    list_display = ("comment", "author", "content", "created_at")


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("comment", "user", "created_at")


class ReplyLikeAdmin(admin.ModelAdmin):
    list_display = ("reply", "user", "created_at")


class FollowerAdmin(admin.ModelAdmin):
    list_display = ("user", "followed", "created_at")


admin.site.register(Post, PostAdmin)
admin.site.register(Media)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(ReplyLike, ReplyLikeAdmin)
admin.site.register(Follower, FollowerAdmin)
