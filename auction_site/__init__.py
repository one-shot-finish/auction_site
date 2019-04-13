from django.apps import AppConfig


class AuctionSiteAppConfig(AppConfig):
    name = 'auction_site'
    label = 'auction_site'
    verbose_name = 'AuctionSite'

    def ready(self):
        import auction_site.signals

default_app_config = 'auction_site.AuctionSiteAppConfig'