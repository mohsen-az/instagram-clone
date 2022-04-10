from django.contrib.auth import login, get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DetailView, ListView
from django.core.cache import cache

from relation.models import StatusRequestRelation, Relation
from user.forms import RegistrationForm, LoginForm

User = get_user_model()


class RegisterView(FormView):
    template_name = "user/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("user:auth-login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.cleaned_data.get("user")
        login(request=self.request, user=user, backend=user.backend)
        return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "user/profile_update.html"
    fields = [
        "username", "email",
        "phone_number", "avatar",
        "bio", "privacy",
        "website"
    ]
    success_url = reverse_lazy("user:auth-profile")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDetailView(DetailView):
    model = User
    slug_url_kwarg = "username"
    slug_field = "username"
    template_name = "user/profile.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.get_object()

        context_data.setdefault(
            "posts_count",
            cache.get_or_set(key=f"{user.username}:posts_count", default=user.posts.count()),
        )
        context_data.setdefault(
            "followings_count",
            cache.get_or_set(
                key=f"{user.username}:followings_count",
                default=user.followings.filter(status=StatusRequestRelation.ACCEPTED).count(),
                timeout=100
            )
        )
        context_data.setdefault(
            "followers_count",
            cache.get_or_set(
                key=f"{user.username}:followers_count",
                default=user.followers.filter(status=StatusRequestRelation.ACCEPTED).count(),
                timeout=100
            )
        )
        context_data.setdefault(
            "is_following",
            Relation.objects.filter(following=self.request.user, follower=user,
                                    status=StatusRequestRelation.ACCEPTED).exists()
        )
        context_data.setdefault(
            "is_send",
            Relation.objects.filter(following=self.request.user, follower=user,
                                    status=StatusRequestRelation.SEND).exists()
        )
        return context_data


class FollowingListView(ListView):
    model = Relation
    template_name = "user/following.html"
    context_object_name = "followings"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return queryset.filter(following=user, status=StatusRequestRelation.ACCEPTED)


class FollowerListView(ListView):
    model = Relation
    template_name = "user/follower.html"
    context_object_name = "followers"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return queryset.filter(follower=user, status=StatusRequestRelation.ACCEPTED)


class InvitationListView(ListView):
    model = Relation
    template_name = "user/invitation.html"
    context_object_name = "invitations"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return queryset.filter(follower=user, status=StatusRequestRelation.SEND)
