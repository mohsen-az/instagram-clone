from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.api.permissions import IsOwnerPermission, IsPublicPermission, RelationExistPermission
from activity.models import Comment, Like
from activity.api import serializers
from content.models import Post


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer
    permission_classes = [
        IsAuthenticated,
        (IsOwnerPermission | IsPublicPermission | RelationExistPermission),
    ]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        serializer.save(user=self.request.user, post=post)


class LikeAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        (IsOwnerPermission | IsPublicPermission | RelationExistPermission),
    ]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("pk")

        post = get_object_or_404(Post, pk=post_id)

        like_qs = Like.objects.filter(
            user=request.user,
            post=post
        )

        if not like_qs.exists():
            Like.objects.create(user=request.user, post=post)
            return Response(
                {"detail": "Like post successfully done."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "This post has already been liked by you"},
            status=status.HTTP_200_OK
        )


class UnLikeAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        (IsOwnerPermission | IsPublicPermission | RelationExistPermission),
    ]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("pk")

        post = get_object_or_404(Post, pk=post_id)

        like_qs = Like.objects.filter(
            user=request.user,
            post=post
        )

        if like_qs.exists():
            like_qs.delete()
            return Response(
                {"detail": "َUnlike post successfully done."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "This post has already been unliked by you"},
            status=status.HTTP_200_OK
        )
