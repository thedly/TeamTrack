from LeaveManager.models import *
from TaskManager.models import TeamtrackNotifications
from django.db.models.signals import post_save, pre_save
import logging
from django.http import HttpResponse
log = logging.getLogger(__name__)


def NotifyUser(sender, instance, **kwargs):
    log.debug("NotifyUserOnLeaveResponse signal called")
    modelName = sender.__name__
    OldLeavesObj = LeavemanagerLeaves.objects.get(pk=instance.Id)
    message = "new notification"
    try:
        TeamtrackNotificationsObj = TeamtrackNotifications(message=message, fromwhom=ExtendedUser.objects.get(pk=1), towhom=ExtendedUser.objects.get(pk=1), link="some link", modelname=modelName, rowid=instance.Id)
        TeamtrackNotificationsObj.save()
    except Exception as ex:
        log.debug(ex.message)
    return HttpResponse("successfully called signal")



post_save.connect(receiver=NotifyUser, sender=LeavemanagerLeaves)


