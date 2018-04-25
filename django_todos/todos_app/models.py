from django.db import models
from model_utils.models import TimeStampedModel


class Todo(TimeStampedModel):
    class Meta:
        ordering = ['-created']
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
