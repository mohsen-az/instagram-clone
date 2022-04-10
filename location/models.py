from django.db import models
from django.utils.translation import gettext_lazy as _

from lib.common_models import BaseModel


class Location(BaseModel):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=32
    )
    points = models.JSONField(
        verbose_name=_("points"),
        default=dict
    )  # sample: {"lat": 32.543, "long": "332.545"}

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.title
