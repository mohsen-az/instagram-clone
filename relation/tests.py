import random

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from relation.models import Relation, StatusRequestRelation

User = get_user_model()


class RelationModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="hossein",
            email="hossein@gmail.com",
            password="QAZwsx123"
        )
        self.other_user = User.objects.create_user(
            username="ali",
            email="ali@gmail.com",
            password="QAZwsx123"
        )

        self.relation = Relation(
            following=self.user,
            follower=self.other_user
        )

    def test_relation_model_representation(self):
        self.assertEqual(
            self.relation.__str__(),
            f'{self.relation.following.username} >> {self.relation.follower.username} | {self.relation.get_status_display()}'
        )


class FollowUnfollowTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="hossein",
            email="hossein@gmail.com",
            password="QAZwsx123"
        )
        self.other_user = User.objects.create_user(
            username="ali",
            email="ali@gmail.com",
            password="QAZwsx123"
        )

    def test_follow_user_api_view(self):
        # Follow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, 401, msg="API is not for authenticated users only.")

        # Follow api request
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk + random.randint(1, 50)}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Follow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.user.pk}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Follow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Follow api request again
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user_api_view(self):
        # Unfollow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/unfollow/"
        )
        self.assertEqual(response.status_code, 401, msg="API is not for authenticated users only.")

        # Unfollow api request
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk + random.randint(1, 50)}/unfollow/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Unfollow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.user.pk}/unfollow/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Follow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Unfollow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/unfollow/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AcceptRejectTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="hossein",
            email="hossein@gmail.com",
            password="QAZwsx123"
        )
        self.other_user = User.objects.create_user(
            username="ali",
            email="ali@gmail.com",
            password="QAZwsx123"
        )

    def test_accept_invitation_api_view(self):
        # Follow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, 401, msg="API is not for authenticated users only.")

        # Follow api request
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Accept api request
        relation = Relation.objects.filter(
            following=self.user,
            follower=self.other_user,
            status=StatusRequestRelation.SEND
        ).first()
        response = self.client.post(
            path=f"/api/relation/friendships/{relation.pk}/accept/"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Unfollow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/unfollow/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reject_invitation_api_view(self):
        # Follow api request
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, 401, msg="API is not for authenticated users only.")

        # Follow api request
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/relation/friendships/{self.other_user.pk}/follow/"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Reject api request
        relation = Relation.objects.filter(
            following=self.user,
            follower=self.other_user,
            status=StatusRequestRelation.SEND
        ).first()
        response = self.client.post(
            path=f"/api/relation/friendships/{relation.pk}/reject/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
