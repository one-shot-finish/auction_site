from django.db import models
import datetime
from users.models import User

class Item(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    base_amount = models.FloatField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def winner_name(self):
        if self.winner is not None:
            return self.winner.full_name
        else:
            return ''

    def winner_email(self):
        if self.winner is not None:
            return self.winner.email
        else:
            return ''

    class Meta:
        ordering = ['-created_at', '-updated_at']