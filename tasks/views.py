from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Tasks
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(owner=self.request.user)


class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        task_id = instance.id

        self.perform_destroy(instance)

        return Response(
            {"message": f"Task number {task_id} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class TaskUpdateStatusView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()

        new_status = request.data.get('status')
        valid_status = [
            Tasks.Status.PROGRESS, Tasks.Status.DONE, Tasks.Status.CANCELLED, Tasks.Status.POSTPONED, Tasks.Status.EXPIRED
        ]

        if new_status not in valid_status:
            return Response({'error': "Estado no válido."}, status=400)

        task.status = new_status
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data)
