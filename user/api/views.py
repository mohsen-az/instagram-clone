from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from user.api import serializers

User = get_user_model()


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return serializers.UserUpdateSerializer
        return super().get_serializer_class()

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {"pk": self.request.user.pk}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "username"
    lookup_field = "username"
