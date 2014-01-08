from TaskManager.models import TaskTrack,Tasks,graphData
from django.db.models.signals import post_save
import logging
import TaskManager.config as config

log = logging.getLogger(__name__)
log.debug("signals page")

def taskUpdate(sender,instance,**kwargs):
    log.info("Signal was called")
    
    oldData = Tasks.objects.get(pk=instance.id)
    if(instance.Status != oldData.Status):
        d = oldData.StartDate
        Hours = (d.hour + d.minute / 60. + d.second / 3600)
        propInv = config.GRAPH_DATA.pop('Investigation')*Hours
        propDev = config.GRAPH_DATA.pop('Development')*Hours
        propTes = config.GRAPH_DATA.pop('Testing')*Hours
        propMer = config.GRAPH_DATA.pop('Merging')*Hours
        propArr = [propInv,propDev,propTes,propMer]
        
        
        graph = graphData(taskid=instance,proposedPlot=propArr,processTPlot="z")
        graph.save()
   
    track = TaskTrack(project=instance.ProjectId,taskid=instance,status=instance.Status,owner=instance.Owner)
    track.save()


post_save.connect(receiver=taskUpdate, sender=Tasks)    