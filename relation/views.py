from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from relation.models import Relation, StatusRequestRelation

User = get_user_model()


class BaseFollowUnFollowView(View):
    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs.get("username"))
        except User.DoesNotExists:
            raise Http404
        else:
            return user


class FollowView(BaseFollowUnFollowView):

    def post(self, request, *args, **kwargs):
        following = request.user
        follower = self.get_object()

        if following == follower:
            return redirect("profile", follower.username)

        relation_qs = Relation.objects.filter(
            following=following,
            follower=follower
        )

        if not relation_qs.exists():
            Relation.objects.get_or_create(following=following, follower=follower)
        return redirect("profile", follower.username)


class UnFollowView(BaseFollowUnFollowView):

    def post(self, request, *args, **kwargs):
        following = request.user
        follower = self.get_object()

        if following == follower:
            return redirect("profile", follower.username)

        relation_qs = Relation.objects.filter(
            following=following,
            follower=follower,
            status=StatusRequestRelation.ACCEPTED
        )

        if relation_qs.exists():
            relation_qs.delete()
            cache.decr(f"{following.username}:followings_count")
            cache.decr(f"{follower.username}:followers_count")

        return redirect("profile", follower.username)


class AcceptInvitationView(BaseFollowUnFollowView):

    def post(self, request, *args, **kwargs):
        following = self.get_object()
        follower = request.user

        if following == follower:
            return redirect("profile", follower.username)

        relation = get_object_or_404(
            Relation, following=following, follower=follower, status=StatusRequestRelation.SEND
        )
        relation.status = StatusRequestRelation.ACCEPTED
        relation.save()
        cache.incr(f"{following.username}:followings_count")
        cache.incr(f"{follower.username}:followers_count")
        return redirect("invitation", follower.username)


class RejectInvitationView(BaseFollowUnFollowView):

    def post(self, request, *args, **kwargs):
        following = self.get_object()
        follower = request.user

        if following == follower:
            return redirect("profile", follower.username)

        relation = get_object_or_404(
            Relation, following=following, follower=follower, status=StatusRequestRelation.SEND
        )
        relation.delete()

        return redirect("invitation", follower.username)
