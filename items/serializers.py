from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'name',
            'description',
            'start_time',
            'end_time',
            'base_amount',
            'winner_name',
            'winner_email',
            'image_url',
        )