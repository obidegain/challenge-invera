from django.contrib import admin
from .models import Tasks

@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'priority', 'status', 'created', 'deadline')
    list_filter = ('status', 'priority', 'deadline', 'created')
    search_fields = ('title', 'description', 'owner__username')