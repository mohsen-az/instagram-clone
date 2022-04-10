from django.contrib import admin

from content.models import Post, PostMedia, Tag, PostTag, TaggedUser


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1


class PostTagInline(admin.TabularInline):
    model = PostTag
    extra = 1


class TaggedUserInline(admin.TabularInline):
    model = TaggedUser
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostMediaInline, PostTagInline, TaggedUserInline]
    list_display = ['user', 'location', 'created_time']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time']
