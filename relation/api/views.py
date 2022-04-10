from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from relation.models import Relation, StatusRequestRelation
from relation.api import serializers

User = get_user_model()


class FollowerListAPIView(generics.ListAPIView):
    queryset = Relation.objects.all()
    serializer_class = serializers.FollowerListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            follower=self.request.user,
            status=StatusRequestRelation.ACCEPTED
        )


class FollowingListAPIView(generics.ListAPIView):
    queryset = Relation.objects.all()
    serializer_class = serializers.FollowingListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            following=self.request.user,
            status=StatusRequestRelation.ACCEPTED
        )


class InvitationListAPIView(generics.ListAPIView):
    queryset = Relation.objects.all()
    serializer_class = serializers.InvitationListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            follower=self.request.user,
            status=StatusRequestRelation.SEND
        )


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        follower_id = kwargs.get("pk")

        following = request.user
        follower = get_object_or_404(User, pk=follower_id)

        if following == follower:
            return Response(
                {"error": "You are not allowed to do this action."},
                status=status.HTTP_400_BAD_REQUEST
            )

        relation_qs = Relation.objects.filter(
            following=following,
            follower=follower
        )

        if not relation_qs.exists():
            Relation.objects.create(following=following, follower=follower)
            return Response(
                {"detail": "A followed request was sent to the user."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "A followed request has already been sent to the user."},
            status=status.HTTP_200_OK
        )


class UnFollowAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        follower_id = kwargs.get("pk")

        following = request.user
        follower = get_object_or_404(User, pk=follower_id)

        if following == follower:
            return Response(
                {"error": "You are not allowed to do this action."},
                status=status.HTTP_400_BAD_REQUEST
            )

        relation_qs = Relation.objects.filter(
            following=following,
            follower=follower,
            status=StatusRequestRelation.ACCEPTED
        )

        if relation_qs.exists():
            relation_qs.delete()
            return Response(
                {"detail": "A unfollowed request was sent to the user."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "A unfollowed request has already been sent to the user."},
            status=status.HTTP_200_OK
        )


class AcceptInvitationAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        relation_id = kwargs.get("pk")

        relation = get_object_or_404(
            Relation,
            pk=relation_id,
            status=StatusRequestRelation.SEND
        )
        relation.status = StatusRequestRelation.ACCEPTED
        relation.save()

        return Response(
            {"detail": "The request was successfully registered."},
            status=status.HTTP_201_CREATED
        )


class RejectInvitationAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        relation_id = kwargs.get("pk")

        relation = get_object_or_404(
            Relation,
            pk=relation_id,
            status=StatusRequestRelation.SEND
        )
        relation.delete()

        return Response(
            {"detail": "The request was rejected."},
            status=status.HTTP_204_NO_CONTENT
        )
