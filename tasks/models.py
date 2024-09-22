from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    class Status(models.TextChoices):
        PROGRESS = 'progress'
        DONE = 'done'
        CANCELLED = 'cancelled'
        POSTPONED = 'postponed'
        EXPIRED = 'expired'

    class Priority(models.TextChoices):
        NORMAL = 'normal'
        HIGH = 'high'
        LOW = 'low'

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(verbose_name="prioridad de la tarea", max_length=20, choices=Priority.choices,default=Priority.NORMAL)
    status = models.CharField(verbose_name="estado de la tarea", max_length=20, choices=Status.choices, default=Status.PROGRESS)
    deadline = models.DateTimeField(verbose_name="fecha límite", null=True, blank=True)

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    def __str__(self):
        return f'{self.title} - {self.deadline} - {self.status}'
