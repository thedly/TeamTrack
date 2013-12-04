from django_cron import CronJobBase, Schedule
import logging
log = logging.getLogger(__name__)
import datetime

class DailyUpdates(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    #RUN_AT_TIMES = ['6:30']
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)#, run_at_times=RUN_AT_TIMES)
    code = 'cron.DailyUpdates'    # a unique code
    def do(self):
        log.info("Cron was called at %s"%datetime.datetime.now())