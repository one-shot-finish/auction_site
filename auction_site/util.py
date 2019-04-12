from dateutil.parser import parse
import pytz

class Util:
    def fetch_date(moment):
        utc = pytz.UTC
        return utc.localize(moment).replace(tzinfo=utc)