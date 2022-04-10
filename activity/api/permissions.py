from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission

from content.models import Post
from relation.models import Relation, StatusRequestRelation
from user.models import Privacy

User = get_user_model()


class RelationExistPermission(BasePermission):
    message = _('You have not access this post.')

    def has_permission(self, request, view):
        post = Post.objects.filter(pk=view.kwargs.get("pk")).first()
        relation_exists = Relation.objects.filter(
            following=request.user,
            follower=post.user,
            status=StatusRequestRelation.ACCEPTED
        ).exists()
        return bool(post and relation_exists)


class IsOwnerPermission(BasePermission):
    message = _('You have not access this post.')

    def has_permission(self, request, view):
        post = Post.objects.filter(pk=view.kwargs.get("pk")).first()
        return bool(post and post.user == request.user)


class IsPublicPermission(BasePermission):
    message = _('You have not access this post.')

    def has_permission(self, request, view):
        post = Post.objects.filter(pk=view.kwargs.get("pk")).first()
        return bool(post and post.user.privacy == Privacy.PUBLIC)
