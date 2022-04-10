from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from user.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = [
        "username",
        "email",
        "privacy",
        "is_staff",
        "is_active",
    ]
    list_display_links = ["username"]
    list_filter = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]

    fieldsets = (
        (_("Login Credentials"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email", "phone_number",)}),
        (_("Profile info"), {"fields": ("avatar", "bio", "website", "privacy", "is_verified",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = [
        "email",
        "username",
    ]


admin.site.register(User, UserAdmin)
