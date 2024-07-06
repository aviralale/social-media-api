from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import random


def get_random_default_pfp():
    peep_count = 105
    return f"user_avatar/peep-{random.randint(1, peep_count)}.jpg"


class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, username, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, username, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(
            email, first_name, last_name, username, password, **extra_fields
        )


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    profile_pic = models.ImageField(
        upload_to="media/user_avatar",
        null=True,
        blank=True,
        default=get_random_default_pfp,
    )
    cover_pic = models.ImageField(
        upload_to="media/user_cover_pic",
        null=True,
        blank=True,
        default=get_random_default_pfp,
    )
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    bio = models.TextField(max_length=103, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "email"]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()
