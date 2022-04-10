from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status

from rest_framework.test import APIClient

from activity.models import Comment, Like
from content.models import Post
from location.models import Location
from relation.models import Relation, StatusRequestRelation
from user.models import Privacy

User = get_user_model()


class CommentModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="hossein",
            email="hossein@gmail.com",
            password="QAZwsx123"
        )
        self.location = Location.objects.create(
            title="Isfahan",
            points={"lat": 123, "long": 123}
        )
        self.post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.user,
            location=self.location
        )
        self.comment = Comment.objects.create(
            caption="Sample Caption Comment",
            user=self.user,
            post=self.post,
            reply_to=None
        )

    def test_comment_model_representation(self):
        self.assertEqual(self.comment.__str__(), self.comment.caption)


class LikeModelTestCase(TestCase):

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
        self.location = Location.objects.create(
            title="Isfahan",
            points={"lat": 123, "long": 123}
        )
        self.post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.user,
            location=self.location
        )
        self.like = Like.objects.create(
            user=self.other_user,
            post=self.post
        )

    def test_like_model_representation(self):
        self.assertEqual(self.like.__str__(), f"{self.like.user.username} >> {self.like.post.pk}")


class CreateCommentTestCase(TestCase):

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
            username="mark",
            email="mark@gmail.com",
            password="QAZwsx123",
            privacy=Privacy.PRIVATE
        )

        self.relation = Relation.objects.create(
            following=self.user,
            follower=self.an_other_user,
            status=StatusRequestRelation.ACCEPTED
        )

        self.location = Location.objects.create(
            title="Tehran",
            points={"lat": 32.543, "long": 332.545}
        )
        self.post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.user,
            location=self.location
        )

        self.an_other_post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.an_other_user,
            location=self.location
        )

    def test_post_existence(self):
        self.assertTrue(Post.objects.exists())
        self.assertEqual(Post.objects.count(), 2)

    def test_comment_creation_api_view(self):
        data = {"caption": "Sample Caption Comment", "reply_to": None}

        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Status code is wrong.")

        self.assertEqual(Comment.objects.count(), 1)

        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            path=f"/api/activity/comments/{self.an_other_post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/activity/comments/{self.an_other_post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)


class CreateReplyCommentTestCase(TestCase):

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

        self.location = Location.objects.create(
            title="Tehran",
            points={"lat": 32.543, "long": 332.545}
        )
        self.post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.user,
            location=self.location
        )
        self.other_post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.user,
            location=self.location
        )

    def test_post_existence(self):
        self.assertTrue(Post.objects.exists())
        self.assertEqual(Post.objects.count(), 2)

    def test_reply_comment_creation_api_view(self):
        data = {"caption": "Sample Caption Comment", "reply_to": None}

        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Status code is wrong.")
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        data = {"caption": "Sample Caption Comment", "reply_to": comment.pk}

        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Status code is wrong.")

        reply_comment = Comment.objects.filter(reply_to__isnull=False).first()

        data = {"caption": "Sample Caption Comment", "reply_to": reply_comment.pk}

        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_same_post_and_comment_creation_api_view(self):
        data = {"caption": "Sample Caption Comment", "reply_to": None}

        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="API is not for authenticated users only.")

        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            path=f"/api/activity/comments/{self.post.pk}/add/",
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Status code is wrong.")
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        data = {"caption": "Sample Caption Comment", "reply_to": comment.pk}

        response = self.client.post(
            path=f"/api/activity/comments/{self.other_post.pk}/add/",
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LikeUnlikeTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="hossein",
            email="hossein@gmail.com",
            password="QAZwsx123"
        )
        self.location = Location.objects.create(
            title="Tehran",
            points={"lat": 32.543, "long": 332.545}
        )
        self.post = Post.objects.create(
            caption="Sample Caption Post",
            user=self.user,
            location=self.location
        )

    def test_like_post_api_view(self):
        # Like api request
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/like/",
        )
        self.assertEqual(response.status_code, 401, msg="API is not for authenticated users only.")

        # Like api request
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/like/",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Like api request again
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/like/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_post_api_view(self):
        # Unlike api request
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/unlike/",
        )
        self.assertEqual(response.status_code, 401, msg="API is not for authenticated users only.")

        # Like api request
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/like/",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Unlike api request
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/unlike/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Unlike api request again
        response = self.client.post(
            path=f"/api/activity/likes/{self.post.pk}/unlike/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
