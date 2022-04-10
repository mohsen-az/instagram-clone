from django.contrib import admin

from relation.models import Relation


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ["following", "follower", "status", "created_time"]
    list_editable = ["status"]
