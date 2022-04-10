from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission

from relation.models import Relation, StatusRequestRelation
from user.models import Privacy

User = get_user_model()


class RelationExistPermission(BasePermission):
    message = _('You have not access this account/post.')

    def has_permission(self, request, view):
        user = User.objects.filter(username=view.kwargs.get("username")).first()
        if user:
            relation_exists = Relation.objects.filter(
                following=request.user,
                follower=user,
                status=StatusRequestRelation.ACCEPTED
            ).exists()
            return bool(user and relation_exists)
        return False


class IsOwnerPermission(BasePermission):
    message = _('You have not access this account/post.')

    def has_permission(self, request, view):
        user = User.objects.filter(username=view.kwargs.get("username")).first()
        return bool(user and request.user == user)


class IsPublicPermission(BasePermission):
    message = _('You have not access this account/post.')

    def has_permission(self, request, view):
        user = User.objects.filter(username=view.kwargs.get("username")).first()
        return bool(user and user.privacy == Privacy.PUBLIC)
