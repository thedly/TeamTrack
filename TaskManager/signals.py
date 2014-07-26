from TaskManager.models import Tasks, TaskmanagerTasktimeline
from django.db.models.signals import post_save
import logging

#log = logging.getLogger(__name__)
#log.debug("signals page")

#def taskUpdate(sender,instance,**kwargs):




#post_save.connect(receiver=taskUpdate, sender=Tasks)