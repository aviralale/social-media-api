from django.db import models
from account.models import User
from django.core.exceptions import ValidationError


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]

    def media_count(self):
        if self.pk:
            return self.media.count()
        return 0

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    def clean(self):
        if self.media_count() > 10:
            raise ValidationError("A post cannot have more than 10 media files.")


class Media(models.Model):
    post = models.ForeignKey(Post, related_name="media", on_delete=models.CASCADE)
    file = models.FileField(upload_to="media/posts/")

    def save(self, *args, **kwargs):
        if self.post.pk and self.post.media_count() >= 10:
            raise ValidationError("A post cannot have more than 10 media files.")
        super().save(*args, **kwargs)

    @property
    def author(self):
        return self.post.author


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def reply_count(self):
        return self.replies.count()

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return self.content[:20]


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, related_name="replies", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return self.content[:20]


class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")


class ReplyLike(models.Model):
    reply = models.ForeignKey(Reply, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reply", "user")


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "followed")
