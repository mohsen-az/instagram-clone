from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from activity.models import Comment
from content.models import Post

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        comment_count = options["count"]

        user = User.objects.first()
        if user is None:
            user = User.objects.create_user(
                username="test",
                email="test@mail.com",
                password="QAZwsx123"
            )

        post = Post.objects.filter(user=user).first()
        if post is None:
            post = Post.objects.create(
                user=user,
                caption="Sample caption post"
            )

        for _ in range(comment_count):
            comment = Comment.objects.create(
                user=user,
                post=post,
                caption="Sample caption comment"
            )
            self.stdout.write(self.style.SUCCESS(f"Comment number {comment.pk} added."))
        self.stdout.write(self.style.SUCCESS(f"Successfully creates {comment_count} comments."))
