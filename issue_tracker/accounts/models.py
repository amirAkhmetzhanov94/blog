from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    avatar = models.ImageField(null=True, blank=True,
                               upload_to="avatars", verbose_name="Avatar")
    github_link = models.URLField(null=True, blank=True,
                                  verbose_name="Github Profile")
    about = models.TextField(null=True, blank=True,
                             verbose_name="About")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
