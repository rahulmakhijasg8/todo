from django.contrib import admin
from .models import Task, Tag


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at", "due_date")
    list_filter = ("status", "tags")
    search_fields = ("title", "description")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)


admin.site.register(Task, TaskAdmin)
admin.site.register(Tag)
