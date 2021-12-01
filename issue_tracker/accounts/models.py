from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        on_delete=models.CASCADE,
        verbose_name=_("ProfileUser")
    )
    avatar = models.ImageField(null=True, blank=True,
                               upload_to="avatars", verbose_name=_("ProfileAvatar"))
    github_link = models.URLField(null=True, blank=True,
                                  verbose_name=_("ProfileGithub"))
    about = models.TextField(null=True, blank=True,
                             verbose_name=_("ProfileAbout"))

    class Meta:
        verbose_name = _("ProfileVerboseName")
        verbose_name_plural = _("ProfilePluralName")
