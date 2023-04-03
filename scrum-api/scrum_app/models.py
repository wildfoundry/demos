from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
    PRIORITIES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    STAGE = [
        ('TD', 'To Do'),
        ('IP', 'In Progress'),
        ('DN', 'Done'),
    ]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='M')
    stage = models.CharField(max_length=2, choices=STAGE, default='TD')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
