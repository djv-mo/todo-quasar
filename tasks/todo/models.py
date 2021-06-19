from django.db import models


class Todo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
