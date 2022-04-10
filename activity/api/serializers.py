from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from activity.models import Like, Comment
from content.models import Post
from relation.models import Relation, StatusRequestRelation
from user.api.serializers import UserRetrieveSerializer
from user.models import Privacy


class LikeSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer()
    followed = serializers.SerializerMethodField(method_name="get_followed")

    class Meta:
        model = Like
        fields = ["user", "followed"]

    def get_followed(self, obj):
        request = self.context.get("request")
        return Relation.objects.filter(
            following=request.user,
            follower=obj.user,
            status=StatusRequestRelation.ACCEPTED
        ).exists()

    def to_representation(self, instance):
        request = self.context.get("request")
        representation = super().to_representation(instance)

        for key, value in {**representation}.items():
            if key == "user" and value.get("username") == request.user.username:
                followed = representation.pop("followed")

        return representation


class CommentListSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer()
    replies = serializers.SerializerMethodField(method_name="get_replies")

    class Meta:
        model = Comment
        fields = ["pk", "user", "caption", "replies"]

    def get_replies(self, obj):
        reply_comments = obj.replies.all()
        serializer = RepliesCommentListSerializer(instance=reply_comments, many=True)
        return serializer.data


class RepliesCommentListSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer()

    class Meta:
        model = Comment
        fields = ["pk", "user", "caption"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["caption", "reply_to"]

    def validate_reply_to(self, attr):
        view = self.context.get("view")
        post = get_object_or_404(Post, pk=view.kwargs.get("pk"))

        if attr and attr.reply_to is not None:
            raise ValidationError(_('You can not reply to a reply recursively.'))

        if attr and attr.post != post:
            raise ValidationError(_("Post and comment are not the same."))

        return attr
