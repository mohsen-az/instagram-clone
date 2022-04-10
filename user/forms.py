from datetime import datetime, timedelta

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from user.tasks import send_phone_verification_code, send_email_verification_link


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "username"]


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ["email", "username"]


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        help_texts = {
            "username": "",
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords must be match"))
        return password2

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data.get("username"),
            email=cleaned_data.get("email"),
            password=cleaned_data.get("password1")
        )
        # send_confirm_email(user)
        # send_confirm_code(user)
        send_phone_verification_code.delay(username=user.username)
        send_email_verification_link.apply_async({"username": user.username}, queue="high")
        send_email_verification_link.apply_async(
            [user.username],
            queue="mid",
            countdown=10,
            eta=datetime.now() + timedelta(seconds=10)
        )
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

        widgets = {
            "password": forms.PasswordInput
        }

        help_texts = {
            "username": "",
        }

    def clean(self):
        username = self.cleaned_data.get("username")

        user = User.objects.filter(username=username).first()
        if user is None:
            raise forms.ValidationError(_("A user with that username does not exists."))

        # if not user.check_password(password):
        #     raise forms.ValidationError(_("Wrong password."))

        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError(_("Unable login with provided credentials."))
        self.cleaned_data.setdefault("user", user)
        return self.cleaned_data
