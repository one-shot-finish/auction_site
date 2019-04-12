from datetime import datetime
from items.models import Item
from bids.models import Bid
from users.models import User
import smtplib
import auction_site.config as config

class WinnerTask:
    def run(self):
        hour = datetime.now().hour
        start = datetime.now().replace(microsecond=0,second=0,minute=0, hour=hour-1)
        end = datetime.now().replace(microsecond=0,second=0,minute=0)
        completed_items = list(Item.objects.filter(end_date__lte=end, end_date__gt=start).values('id'))
        completed_item_ids = map(lambda x: x['id'], completed_items)
        bids = list(Bid.objects.filter(item_id__in=completed_item_ids).order_by('amount').values('amount', 'item_id', 'user_id', 'id'))
        item_vals = {}
        for bid in bids:
            item_vals[bid['item_id']] = (bid['amount'], bid['user_id'])
            b = Bid.objects.get(pk=bid['id'])
            b.winner_id = bid['user_id']
            b.save()

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
            server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, msg)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")


w = WinnerTask()
w.run()
