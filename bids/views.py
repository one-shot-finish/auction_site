from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BidSerializer
from .models import Bid
from auction_site.util import Util
from items.models import Item
from users.models import User
# Create your views here.
from datetime import datetime

class BidView(APIView):
    def get(self, request):
        success, response = self.authenticate(request)
        if not success:
            return response
        user = response
        bids = Bid.objects.filter(user_id=user.id)
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

    def post(self, request):
        success, response = self.authenticate(request)
        if not success:
            return response


        user = response

        item_id = request.query_params.get('item_id')
        try:
            item = Item.objects.get(pk=item_id)
        except:
            return Response({"message": 'Invalid item', "success": False})

        end_time, start_time = item.end_time, item.start_time
        now = Util.fetch_date(datetime.now())
        if not (start_time <= now <= end_time):
            return Response({"message": "Item not in bidding at current time", "success": False})


        amount = request.query_params.get('amount')
        bid = Bid(user_id=user.id, item_id=item_id, amount=amount)
        bid.save()
        serializer = BidSerializer(bid, many=False)
        data = serializer.data
        data.update({"success": True})
        return Response(data)

    def authenticate(self, request):
        user = None
        try:
            email = request.query_params.get('email').strip().lower()
            user = User.objects.get(email=email)
        except:
            return False, Response({"message": 'Invalid user', "success": False})

        try:
            password = request.query_params.get('password')
            print("PASS", user.password, password)
            if user.password != password:
                raise ""
        except:
            return False, Response({"message": 'Invalid password', "success": False})
        return True, user




