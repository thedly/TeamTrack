from TaskManager.models import TaskTrack,Tasks
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging
log = logging.getLogger(__name__)
log.debug("debug")

def taskUpdate(sender,instance,**kwargs):
    log.info("Signal was called")
    track = TaskTrack(taskid=instance,status=instance.Status,owner=instance.Owner)
    track.save()


post_save.connect(receiver=taskUpdate, sender=Tasks)    