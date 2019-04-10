from django.db import models
import datetime

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at', '-updated_at']