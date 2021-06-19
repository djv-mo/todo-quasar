from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = '__all__'

    def get_created_at(self, instance):
        return instance.created_at.strftime('%B %d %Y')
