from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="auth-register"),
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path("profile/", views.ProfileUpdateView.as_view(), name="auth-profile"),
]
