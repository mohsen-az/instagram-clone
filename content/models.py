from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from location.models import Location
from lib.common_models import BaseModel

User = get_user_model()


class Post(BaseModel):
    caption = models.TextField(
        verbose_name=_("caption"),
        max_length=500,
        blank=True
    )
    user = models.ForeignKey(
        verbose_name=_("user"),
        to=User,
        related_name='posts',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        verbose_name=_("location"),
        to=Location,
        related_name='posts',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-created_time"]

    def __str__(self):
        return f'{self.pk} - {self.user.username} - {self.caption[:30]}'


class MediaType(models.IntegerChoices):
    IMAGE = (1, _("Image"))
    VIDEO = (2, _("Video"))


class PostMedia(BaseModel):
    media_type = models.PositiveSmallIntegerField(
        verbose_name=_("media type"),
        choices=MediaType.choices,
        default=MediaType.IMAGE
    )
    post = models.ForeignKey(
        verbose_name=_("post"),
        to=Post,
        related_name='media',
        on_delete=models.CASCADE
    )
    media_file = models.FileField(
        verbose_name=_("media file"),
        upload_to='content/post/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=('jpg', 'jpeg', 'mp4', 'wmv', 'flv', 'png')
            )
        ]
    )

    class Meta:
        verbose_name = _("Post Media")
        verbose_name_plural = _("Post Media")

    def __str__(self):
        return f'{self.post} - {self.get_media_type_display()}'


class TaggedUser(BaseModel):
    user = models.ForeignKey(
        verbose_name=_("user"),
        to=User,
        related_name='tagged_posts',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        verbose_name=_("post"),
        to=Post,
        related_name='tagged_users',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Tagged User")
        verbose_name_plural = _("Tagged Users")

    def __str__(self):
        return f'{self.post} - {self.post}'


class Tag(BaseModel):
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f'{self.title}'


class PostTag(BaseModel):
    post = models.ForeignKey(
        verbose_name=_("post"),
        to=Post,
        related_name='hashtags',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        verbose_name=_("tag"),
        to=Tag,
        related_name='posts',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Post Tag")
        verbose_name_plural = _("Post Tags")

    def __str__(self):
        return f'{self.post} - {self.tag}'
