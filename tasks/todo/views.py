from datetime import date
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    # today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    # today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    queryset = Todo.objects.all().order_by('-created_at').filter(created_at__startswith=date.today())
    serializer_class = TodoSerializer
