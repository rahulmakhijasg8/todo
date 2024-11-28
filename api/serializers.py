from rest_framework import serializers
from .models import Task, Tag
from django.utils import timezone


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class TaskSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "tags",
            "due_date",
            "status",
        ]

    def validate(self, data):
        if "due_date" in data and data["due_date"]:
            data["created_at"] = timezone.now()
            if data["due_date"] < data["created_at"]:
                raise serializers.ValidationError
            ("Due Date cannot be in the past.")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = [tag["name"] for tag in data["tags"]]
        return data

    def to_internal_value(self, data):
        data1 = super().to_internal_value(data)
        if "tags" in data:
            data1["tags"] = [
                Tag.objects.get_or_create(name=tag)[0] for tag in data["tags"]
            ]
        return data1
