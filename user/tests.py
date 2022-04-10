from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient

from relation.api import serializers
from relation.models import Relation, StatusRequestRelation
from user.api.serializers import UserSerializer

User = get_user_model()


class UserModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="hossein",
            email="hossein@gmail.com",
            password="QAZwsx123"
        )

    def test_user_model_get_full_name_method(self):
        self.assertEqual(self.user.get_full_name(), self.user.username)

    def test_user_model_get_short_name_method(self):
        self.assertEqual(self.user.get_short_name(), self.user.username)


class ProfileTestCase(TestCase):
    fixtures = ["fixtures.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.first()

    def test_profile_api_view(self):
        response = self.client.get(
            path=f"/api/auth/profile/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        user = User.objects.filter(
            username=self.user.username
        ).first()
        serializer = UserSerializer(instance=user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/auth/profile/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(response.data["username"], serializer.data["username"])

    def test_profile_update_api_view(self):
        data = {"bio": "Change bio..."}
        response = self.client.patch(
            path=f"/api/auth/profile/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            path=f"/api/auth/profile/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        user = User.objects.filter(
            username=self.user.username
        ).first()
        serializer = UserSerializer(instance=user)

        self.assertEqual(response.data["bio"], serializer.data["bio"])

    def test_profile_list_follower_api_view(self):
        response = self.client.get(
            path=f"/api/auth/profile/follower/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        followers = Relation.objects.filter(
            follower=self.user,
            status=StatusRequestRelation.ACCEPTED
        )
        serializer = serializers.FollowerListSerializer(instance=followers, many=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/auth/profile/follower/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(len(response.data), len(serializer.data))

    def test_profile_list_following_api_view(self):
        response = self.client.get(
            path=f"/api/auth/profile/following/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        followings = Relation.objects.filter(
            following=self.user,
            status=StatusRequestRelation.ACCEPTED
        )
        serializer = serializers.FollowingListSerializer(instance=followings, many=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/auth/profile/following/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(len(response.data), len(serializer.data))

    def test_profile_list_invitation_api_view(self):
        response = self.client.get(
            path=f"/api/auth/profile/invitation/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        invitations = Relation.objects.filter(
            follower=self.user,
            status=StatusRequestRelation.SEND
        )
        serializer = serializers.InvitationListSerializer(instance=invitations, many=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/auth/profile/invitation/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(len(response.data), len(serializer.data))
