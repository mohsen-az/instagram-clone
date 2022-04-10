from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

from activity.api.serializers import LikeSerializer, CommentListSerializer
from content.api import serializers
from content.models import Post
from content.api.permissions import IsOwnerPermission, IsPublicPermission, RelationExistPermission


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostListSerializer
    permission_classes = [
        IsAuthenticated,
        (IsOwnerPermission | IsPublicPermission | RelationExistPermission)
    ]

    lookup_url_kwarg = "pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username=self.kwargs.get("username"))

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PostRetrieveSerializer
        elif self.action == "get_like_list":
            return LikeSerializer
        elif self.action == "get_comment_list":
            return CommentListSerializer
        return self.serializer_class

    @action(methods=["GET"], detail=True, url_path="likes")
    def get_like_list(self, request, *args, **kwargs):
        post = self.get_object()
        queryset = post.likes.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=True, url_path="comments")
    def get_comment_list(self, request, *args, **kwargs):
        post = self.get_object()
        queryset = post.comments.filter(reply_to__isnull=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
