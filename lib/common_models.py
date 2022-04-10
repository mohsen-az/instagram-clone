from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(
        verbose_name=_("created time"),
        auto_now_add=True
    )
    updated_time = models.DateTimeField(
        verbose_name=_("updated time"),
        auto_now=True
    )

    class Meta:
        abstract = True