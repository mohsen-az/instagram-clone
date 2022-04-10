from rest_framework import serializers

from content.models import Post, PostMedia, TaggedUser, PostTag
from location.api.serializers import LocationSerializer
from user.api.serializers import UserRetrieveSerializer


class PostMediaSerializer(serializers.ModelSerializer):
    media_type = serializers.CharField(source="get_media_type_display")

    class Meta:
        model = PostMedia
        fields = ["media_type", "media_file"]


class TaggedUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = TaggedUser
        fields = ["user"]


class HashTagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source="tag.title")

    class Meta:
        model = PostTag
        fields = ["tag"]


class PostListSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True)

    class Meta:
        model = Post
        fields = ["pk", "media"]


class PostRetrieveSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer()
    location = LocationSerializer()
    media = PostMediaSerializer(many=True)
    tagged_users = TaggedUserSerializer(many=True)
    hashtags = HashTagSerializer(many=True)

    count_likes = serializers.SerializerMethodField(method_name="get_count_likes")
    count_comments = serializers.SerializerMethodField(method_name="get_count_comments")

    class Meta:
        model = Post
        fields = [
            "pk", "user", "caption",
            "location", "media",
            "tagged_users", "hashtags",
            "count_likes", "count_comments"
        ]

    def get_count_likes(self, obj):
        return obj.likes.count()

    def get_count_comments(self, obj):
        return obj.comments.count()


class TaggedUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedUser
        fields = ["user"]


class HashTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ["tag"]


class PostMediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ["media_type", "media_file"]


class PostCreateSerializer(serializers.ModelSerializer):
    media = PostMediaCreateSerializer(many=True)
    tagged_users = TaggedUserCreateSerializer(many=True, required=False)
    hashtags = HashTagCreateSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ["caption", "location", "media", "tagged_users", "hashtags"]

    def create(self, validated_data):
        """
        caption: str
        location: int

        tagged_users[0]user: int
        tagged_users[1]user: int
        tagged_users[2]user: int

        hashtags[0]tag: int
        hashtags[1]tag: int
        hashtags[2]tag: int

        media[0]media_type: int
        media[0]media_file: file

        media[1]media_type: int
        media[1]media_file: file
        """
        tagged_users = validated_data.pop("tagged_users", [])
        hashtags = validated_data.pop("hashtags", [])
        media = validated_data.pop("media", [])

        instance = super().create(validated_data)

        for tagged_user in tagged_users:
            serializer = TaggedUserCreateSerializer(data={"user": tagged_user["user"].pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(post=instance)

        for hashtag in hashtags:
            serializer = HashTagCreateSerializer(data={"tag": hashtag["tag"].pk})
            serializer.is_valid(raise_exception=True)
            serializer.save(post=instance)

        for post_media in media:
            serializer = PostMediaCreateSerializer(
                data={"media_type": post_media["media_type"], "media_file": post_media["media_file"]}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(post=instance)

        return instance
