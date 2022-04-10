from rest_framework import serializers

from relation.models import Relation, StatusRequestRelation
from user.api.serializers import UserRetrieveSerializer


class FollowerListSerializer(serializers.ModelSerializer):
    following = serializers.CharField(source="following.username")
    followed_back = serializers.SerializerMethodField(method_name="get_followed_back")

    class Meta:
        model = Relation
        fields = ["following", "followed_back"]

    def get_followed_back(self, obj):
        return Relation.objects.filter(
            following=obj.follower,
            follower=obj.following,
            status=StatusRequestRelation.ACCEPTED
        ).exists()


class FollowingListSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source="follower.username")
    followed_back = serializers.SerializerMethodField(method_name="get_followed_back")

    class Meta:
        model = Relation
        fields = ["follower", "followed_back"]

    def get_followed_back(self, obj):
        return Relation.objects.filter(
            following=obj.follower,
            follower=obj.following,
            status=StatusRequestRelation.ACCEPTED
        ).exists()


class InvitationListSerializer(serializers.ModelSerializer):
    following = UserRetrieveSerializer()

    class Meta:
        model = Relation
        fields = ["pk", "following"]
