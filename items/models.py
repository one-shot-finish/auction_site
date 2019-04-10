from django.db import models
import datetime
from users.models import User

class Item(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    base_amount = models.FloatField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at', '-updated_at']