from django_cron import CronJobBase, Schedule
from .task import WinnerTask

class WinnerCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'auction_site.winner_cron_job'

    def do(self):
        WinnerTask().do()
