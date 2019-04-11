from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer
from .models import Item
from django.db.models import Q
import datetime, json
# Create your views here.

class ItemView(APIView):
    def get(self, request):
        # body_unicode = request.data

        now = datetime.datetime.now()
        if request.query_params.get('type') == 'previous':
            items = Item.objects.filter(Q(start_time__lt=now.date())).order_by('-start_time')
        elif request.query_params.get('type') == 'upcoming':
            items = Item.objects.filter(Q(start_time__gt=now.date())).order_by('-start_time')
        else:
            items = Item.objects.all()

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)