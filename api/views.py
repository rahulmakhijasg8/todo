from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated


class TaskViewset(ModelViewSet):

    queryset = Task.objects.prefetch_related("tags").all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
