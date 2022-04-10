import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from activity.api.serializers import LikeSerializer
from content.api import serializers
from content.api.serializers import TaggedUserCreateSerializer
from content.models import Post, Tag, PostMedia
from location.models import Location

User = get_user_model()


class CreatePostTestCase(TestCase):

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
        self.an_other_user = User.objects.create_user(
            username="sara",
            email="sara@gmail.com",
            password="QAZwsx123"
        )

        self.tag = Tag.objects.create(
            title="7learn"
        )
        self.other_tag = Tag.objects.create(
            title="python"
        )
        self.an_other_tag = Tag.objects.create(
            title="django"
        )

    @unittest.skip(reason="")
    def test_post_creation_api_view(self):
        data = {
            "caption": "Sample Caption Post",
            "tagged_users": [{"user": self.user.pk}, {"user": self.other_user.pk}, {"user": self.an_other_user.pk}],
            "hashtags": [{"tag": self.tag.pk}, {"tag": self.other_tag.pk}, {"tag": self.an_other_tag.pk}]
        }

        response = self.client.post(
            path="/api/content/post/add/",
            data=data,
            format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path="/api/content/post/add/",
            data=data,
            format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostTestCase(TestCase):
    fixtures = ["fixtures.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.first()
        self.post = Post.objects.filter(user=self.user).first()

    def test_post_list_api_view(self):
        # Get API response
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/",
        )
        # Get data from db
        posts = Post.objects.filter(user=self.user)
        serializer = serializers.PostListSerializer(instance=posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(len(response.data), len(serializer.data))

    def test_post_retrieve_list_api_view(self):
        # Get API response
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/{self.post.pk}/",
        )
        # Get data from db
        serializer = serializers.PostRetrieveSerializer(instance=self.post)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/{self.post.pk}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(serializer.data["pk"], response.data["pk"])
        self.assertEqual(serializer.data["user"]["username"], response.data["user"]["username"])

    def test_post_get_likes_list_api_view(self):
        # Get API response
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/{self.post.pk}/likes/",
        )
        # Get data from db
        qs = self.post.likes.all()
        serializer = LikeSerializer(instance=qs, many=True)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/{self.post.pk}/likes/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(len(serializer.data), len(response.data))

    def test_post_get_comments_list_api_view(self):
        # Get API response
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/{self.post.pk}/comments/",
        )
        # Get data from db
        qs = self.post.comments.filter(reply_to__isnull=True)
        serializer = LikeSerializer(instance=qs, many=True)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            path=f"/api/content/{self.user.username}/posts/{self.post.pk}/comments/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Status code is wrong.")

        self.assertEqual(len(serializer.data), len(response.data))
