from BugTracker.models import BugScreenShots, Bug
from django.http import HttpResponse
import logging
import json
import shutil
from TeamTrack.settings import STATIC_URL
log = logging.getLogger(__name__)

def UpdateScreenshots(sender, instance, **kwargs):
    try:
        BugScreenShotsObj = BugScreenShots.objects.filter(imageId=instance.id)
        with open("%s%s" % (STATIC_URL, "Config/BugTrackerConfig.json"), 'r') as BugPathObj:
            BugPathObj = json.loads(BugPathObj)
            TempDestination = "%s" % BugPathObj.BugScreenshotTempFolder
            FinalDestination = instance.imagePath
        for screenshot in BugScreenShotsObj:
            newtempDestination = "%s%s" % (TempDestination, screenshot.imageName)
            shutil.move(FinalDestination, newtempDestination)

        return HttpResponse("Success")
    except Exception as ex:
        log.exception(ex)
        return HttpResponse(ex)
