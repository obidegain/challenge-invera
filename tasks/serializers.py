from rest_framework import serializers
from .models import Tasks

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'status', 'description', 'created', 'deadline', 'owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['title'].required = False