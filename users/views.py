from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from tasks.serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from tasks.models import Tasks

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class GetTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(owner=self.request.user)