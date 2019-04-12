from django.db import models
from users.models import User
from items.models import Item

class Bid(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount)

    def user_detail(self):
        return str(self.user)

    def item_detail(self):
        return str(self.item)

    class Meta:
        ordering = ['-created_at', '-updated_at']