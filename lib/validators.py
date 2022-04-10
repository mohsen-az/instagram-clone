from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^09\d{9}$'

    message = _(
        'Enter a valid phone number.'
    )
    flags = 0
