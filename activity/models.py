from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from content.models import Post
from lib.common_models import BaseModel

User = get_user_model()


class Comment(BaseModel):
    caption = models.TextField()
    user = models.ForeignKey(
        verbose_name=_("user"),
        to=User,
        related_name="comments",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        verbose_name=_("post"),
        to=Post,
        related_name="comments",
        on_delete=models.CASCADE
    )
    reply_to = models.ForeignKey(
        verbose_name=_("reply to"),
        to="self",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.caption


class Like(BaseModel):
    user = models.ForeignKey(
        verbose_name=_("user"),
        to=User,
        related_name='likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        verbose_name=_("post"),
        to=Post,
        related_name='likes',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f'{self.user.username} >> {self.post.pk}'
