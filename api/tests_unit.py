from django.test import TestCase
from .models import Task, Tag
from django.utils import timezone
from .serializers import TaskSerializer
from rest_framework.validators import ValidationError
from django.core.exceptions import ValidationError as vd


class TaskModelTest(TestCase):
    def setUp(self) -> None:
        self.task = Task.objects.create(
            title="Test Task", description="This is a test task", status="OPEN"
        )
        self.tag = Tag.objects.create(name="Urgent")

    def test_task_creation(self):
        self.task.tags.add(self.tag)
        self.assertEqual(self.tag.name, "Urgent")
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "OPEN")
        self.assertEqual(self.task.tags.count(), 1)
        self.assertEqual(self.task.description, "This is a test task")

    def test_task_deletion(self):
        self.task.tags.add(self.tag)

        self.task.delete()
        self.tag.delete()
        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_model(self):
        t = self.task
        self.assertEqual(str(t), "Test Task")

    def test_tag_model(self):
        t = self.tag
        self.assertEqual(str(t), "Urgent")

    def test_due_date_validation(self):
        with self.assertRaises(vd):
            past_task = Task.objects.create(
                title="Past Due Task",
                description="Task with past due date",
                due_date=timezone.now() - timezone.timedelta(days=1),
            )
            past_task.clean()


class TestTaskSerializerValidation(TestCase):
    def setUp(self) -> None:
        self.created_at = timezone.now()
        self.tag = Tag.objects.create(name="Urgent")
        self.valid_task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "created_at": self.created_at,
            "due_date": self.created_at + timezone.timedelta(days=1),
            "tags": [self.tag.name],
        }

        self.invalid_task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "created_at": self.created_at,
            "due_date": self.created_at - timezone.timedelta(days=1),
            "tags": [self.tag.name],
        }

    def test_validation_valid_data(self):
        serializer = TaskSerializer(data=self.valid_task_data)
        serializer.is_valid(raise_exception=True)
        self.assertTrue(serializer.is_valid())

    def test_validation_invalid_data(self):
        serializer = TaskSerializer(data=self.invalid_task_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.assertFalse(serializer.is_valid())


class TestTaskSerializer(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Urgent")
        self.tag2 = Tag.objects.create(name="Important")
        self.task = Task.objects.create(
            title="Test Task",
            description="Test task description",
            status="OPEN",
        )
        self.task.tags.add(self.tag1, self.tag2)

    def test_to_representation(self):
        serializer = TaskSerializer(instance=self.task)
        data = serializer.to_representation(self.task)
        self.assertIn("tags", data)
        self.assertEqual(data["tags"], ["Urgent", "Important"])
