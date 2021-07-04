from datetime import date
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    today = date.today()

    queryset = Todo.objects.all().order_by(
        '-created_at').filter(created_at__day=today.day)
    serializer_class = TodoSerializer
