from random import choice, sample, randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from content.models import PostMedia, Post, Tag
from location.models import Location

User = get_user_model()

SAMPLE_CAPTION = """Lorem ipsum dolor sit amet, vix omittam dissentias signiferumque ne, eos accusata percipitur ne.
Te vero accusam duo, et mea laudem regione conclusionemque, no magna movet euismod nec. Agam antiopam usu ad, 
his clita labitur molestie in. Errem petentium id vis. Et legere interesset est.
"""


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        post_count = options["count"]

        users = User.objects.all()
        media_images = PostMedia.objects.all()
        locations = Location.objects.all()
        tags = Tag.objects.all()

        for _ in range(post_count):
            post = Post.objects.create(
                user=choice(users),
                location=choice(locations),
                caption=SAMPLE_CAPTION
            )
            post.media.add(*sample(list(media_images), randint(1, len(media_images))))
            for _ in range(1, randint(1, len(users))):
                post.tagged_users.create(
                    user=choice(users)
                )
            for _ in range(1, randint(1, len(tags))):
                post.hashtags.create(
                    tag=choice(tags)
                )

            self.stdout.write(self.style.SUCCESS(f"Post number {post.pk} added."))
        self.stdout.write(self.style.SUCCESS(f"Successfully creates {post_count} posts."))
