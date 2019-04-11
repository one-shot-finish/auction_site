from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BidSerializer
from .models import Bid
# Create your views here.

class BidView(APIView):
    def get(self, request):
        bids = Bid.objects.all()
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)