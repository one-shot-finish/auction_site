from rest_framework import serializers
from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = (
            'user_detail',
            'item_detail',
            'amount',
        )