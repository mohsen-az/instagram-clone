from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from lib.common_models import BaseModel

User = get_user_model()


class StatusRequestRelation(models.IntegerChoices):
    SEND = (1, _("Send"))
    ACCEPTED = (2, _("Accepted"))


class Relation(BaseModel):
    following = models.ForeignKey(
        verbose_name=_("following"),
        to=User,
        on_delete=models.CASCADE,
        related_name="followings"
    )  # from_user

    follower = models.ForeignKey(
        verbose_name=_("follower"),
        to=User,
        on_delete=models.CASCADE,
        related_name="followers"
    )  # to_user

    status = models.PositiveSmallIntegerField(
        verbose_name=_("status request relation"),
        choices=StatusRequestRelation.choices,
        default=StatusRequestRelation.SEND
    )

    class Meta:
        verbose_name = _("Relation")
        verbose_name_plural = _("Relations")

    def __str__(self):
        return f'{self.following.username} >> {self.follower.username} | {self.get_status_display()}'
