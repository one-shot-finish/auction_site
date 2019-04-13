from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer
from .models import Item
from bids.models import Bid
from users.models import User
from django.db.models import Q
from auction_site.util import Util
import datetime
# Create your views here.

class ItemView(APIView):
    def get(self, request):
        # body_unicode = request.data

        now = datetime.datetime.now()
        if request.query_params.get('type') == 'previous':
            items = Item.objects.filter(Q(end_time__lt=now.date())).order_by('-end_time')
        elif request.query_params.get('type') == 'upcoming':
            items = Item.objects.filter(Q(end_time__gt=now.date())).order_by('-end_time')
        else:
            items = Item.objects.all()

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class ItemDetail(APIView):
    def get(self, request):
        now = datetime.datetime.now()

        bids = list(Bid.objects.order_by('amount').values('amount', 'item_id', 'user_id'))
        item_vals = {}
        for bid in bids:
            item_vals[bid['item_id']] = (bid['amount'], bid['user_id'])

        items = list(Item.objects.filter(id__in=list(item_vals.keys())).values())
        for item in items:
            amount = item_vals[item['id']][0]
            user_id = item_vals[item['id']][1]

            if item['end_time'] < Util.fetch_date(now):
                item['winner_name'] = User.objects.get(pk=item['winner_id']).full_name
                item['status'] = 'Completed'
                item['sold_amount'] = amount
            else:
                item['user_name'] = User.objects.get(pk=user_id).full_name
                item['status'] = 'Live'
                item['highest_bid_amount'] = amount
        items = [{k: v for k, v in d.items() if k not in ['id', 'created_at', 'updated_at', 'winner_id']} for d in items]
        return Response(items)
