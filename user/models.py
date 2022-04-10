from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.cache import cache

from user.managers import UserManager
from lib.validators import PhoneNumberValidator


class Privacy(models.IntegerChoices):
    PUBLIC = (1, _('Public'))
    PRIVATE = (2, _('Private'))


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    phone_number_validator = PhoneNumberValidator()

    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True
    )

    phone_number = models.CharField(
        verbose_name=_('phone number'),
        max_length=11,
        validators=[phone_number_validator],
        blank=True
    )

    avatar = models.ImageField(
        verbose_name=_('avatar'),
        upload_to='users/avatar/',
        default='sample/avatar.png',
        validators=[
            FileExtensionValidator(
                allowed_extensions=('jpg', 'jpeg', 'png')
            )
        ],
        blank=True,
    )

    bio = models.TextField(
        verbose_name=_('bio'),
        max_length=250,
        blank=True,
    )

    privacy = models.PositiveSmallIntegerField(
        verbose_name=_('privacy'),
        choices=Privacy.choices,
        default=Privacy.PUBLIC,
        help_text='1 -> Public, 2 -> Private'
    )

    website = models.URLField(
        verbose_name=_('website'),
        blank=True,
    )

    is_verified = models.BooleanField(
        verbose_name=_('is verified'),
        default=False
    )

    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username

    def check_verify_code(self, password):
        verification_code = cache.get(f"{self.phone_number}")
        return verification_code == password
