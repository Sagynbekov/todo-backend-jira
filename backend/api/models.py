# backend/api/models.py

from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=128)  # Store Firebase user ID

    def __str__(self):
        return self.name
