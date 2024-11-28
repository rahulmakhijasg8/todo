from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task, Tag
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from .serializers import TaskSerializer
from rest_framework.validators import ValidationError
from django.core.exceptions import ValidationError as vd


class TaskModelTest(TestCase):
    def setUp(self) -> None:
        self.task = Task.objects.create(
            title="Test Task", description="This is a test task", status="OPEN"
        )
        self.tag = Tag.objects.create(name="Urgent")

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


class TestCreateTask(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin", password="12345"
        )
        self.task = Task.objects.create(
            title="Original Task",
            description="This is the original description.",
            status="OPEN",
        )
        self.tag = Tag.objects.create(name="Urgent")

    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()

        response = client.post(
            "/api/tasks/",
            {
                "title": "unittest testing",
                "description": "lets see if it works",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_user_is_authorized_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(
            "/api/tasks/",
            {
                "title": "unittest testing",
                "description": "lets see if it works",
            },
        )
        task = Task.objects.get(id=response.data["id"])
        self.assertEqual(task.title, "unittest testing")
        self.assertEqual(task.tags.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_patch_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        self.task.tags.add(self.tag)
        response = client.put(
            f"/api/tasks/{self.task.id}/",
            {
                "title": "unittest testing",
                "description": "lets see if it works",
                "tags": ["Urgent"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "unittest testing")
        self.assertEqual(self.task.description, "lets see if it works")

    def test_if_delete_returns_204(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete(f"/api/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        with self.assertRaises(Task.DoesNotExist):
            self.task.refresh_from_db()

    def test_if_delete_returns_404_for_nonexistent_task(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete("/api/tasks/999/")

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_create_tags_validation(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(
            "/api/tasks/",
            {
                "title": "unittest testing",
                "description": "lets see if it works",
                "tags": ["Urgent"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_tasks(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/api/tasks/", format="json")
        self.assertEqual(len(response.data), 1)
        Task.objects.create(
            title="Task 1",
            description="Task 1 description",
            due_date=timezone.now() + timezone.timedelta(days=1),
        )
        Task.objects.create(
            title="Task 2",
            description="Task 2 description",
            due_date=timezone.now() + timezone.timedelta(days=1),
        )
        response = client.get("/api/tasks/", format="json")
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
