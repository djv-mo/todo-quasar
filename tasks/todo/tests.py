import json

from django.urls import reverse, resolve

from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import TodoSerializer
from .models import Todo


class TodoTestCase(APITestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title='test_todo')

    def test_todo_model(self):
        assert Todo.__str__(self.todo) == self.todo.title
        assert str(self.todo) == self.todo.title


    def test_todo_list(self):
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.todo.title)

    def test_todo_detail(self):
        response = self.client.get(reverse('todo-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        serializer_data = TodoSerializer(instance=self.todo).data
        self.assertEqual(response_data, serializer_data)

    def test_todo_create(self):
        form = {"title": "first task"}
        response = self.client.post(reverse('todo-list'), form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        todo = Todo.objects.get(title='first task')
        assert todo.title == form['title']

    def test_todo_update(self):
        response = self.client.put(reverse('todo-detail',
                                        kwargs={'pk': 1}),
                                        {'title': 'modified'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'modified')

    def test_todo_delete(self):
        response = self.client.delete(reverse('todo-detail',
                                        kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
