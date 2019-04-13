from items.models import Item
from bids.models import Bid
from users.models import User
import smtplib
import auction_site.config as config
from datetime import datetime, timedelta

class WinnerTask:
    def run(self):
        start = (datetime.now() - timedelta(hours = 1)).replace(microsecond=0,second=0,minute=0)
        end = datetime.now().replace(microsecond=0,second=0,minute=0, hour=datetime.now().hour+1)
        completed_items = list(Item.objects.filter(end_time__lte=end, end_time__gt=start).values('id'))
        completed_item_ids = list(map(lambda x: x['id'], completed_items))
        bids = list(Bid.objects.filter(item_id__in=completed_item_ids).order_by('amount').values('amount', 'item_id', 'user_id', 'id'))
        item_vals = {}
        for bid in bids:
            item_vals[bid['item_id']] = (bid['amount'], bid['user_id'])

        items = list(Item.objects.filter(id__in=list(item_vals.keys())).values())

        for item_i in items:
            item = Item.objects.get(pk=item_i['id'])
            item.winner_id = item_vals[item_i['id']][1]
            item.save()

        self.send_emails(item_vals)


    def send_emails(self, item_vals):
        try:
            server = smtplib.SMTP('smtp.outlook.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.PASSWORD)
            subject='Auction Results'
            msg = "Dear All\n\nItem\tWinner\tAmount\n"
            for key, val in item_vals.items():
                item_name = Item.objects.get(pk=key).name
                amount = str(val[0])
                winner_name = User.objects.get(pk=val[1]).full_name
                msg += item_name + "\t" + amount + "\t" + winner_name + "\n"
            msg += "\nRegards"
            msg ='Subject: {}\n\n{}'.format(subject, msg)
            emails = list(User.objects.values('email'))
            tos = list(map(lambda x:x['email'], emails))
            server.sendmail(config.EMAIL_ADDRESS, tos, msg)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")

