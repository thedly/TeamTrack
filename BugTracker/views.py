# Create your views here.
from django.views.generic.base import TemplateView
from BugTracker.forms import CreateBugForm
from BugTracker.models import Bug, BugScreenShots
from TaskManager.models import Tasks, TaskStatus, TaskmanagerTasktimeline, ExtendedUser
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime
from TeamTrack.settings import STATIC_URL
import logging
import os
import json
import redis
log = logging.getLogger(__name__)
from mimetypes import MimeTypes

class BugView(TemplateView):
    template_name = "bugs.html"

    def get_context_data(self, **kwargs):
        context = super(BugView, self).get_context_data(**kwargs)
        context['BugForm'] = CreateBugForm()
        context['Bugs'] = Bug.objects.all()
        return context

def RaiseABug(request):
    try:
        obj = Tasks.objects.get(pk=request.POST['TaskId'])
        obj.Status = TaskStatus.objects.get(pk=3)
        BugObj = Bug(title=request.POST['Title'], taskid=obj, description=request.POST['Description'], status=obj.Status, owner=ExtendedUser.objects.get(pk=request.user))
        BugObj.save()
        obj.save()
        project = obj.ProjectId
        timelineObj = TaskmanagerTasktimeline(project=project, title=request.POST['Title'], taskid=obj, status=obj.Status, owner=ExtendedUser.objects.get(pk=request.user.id), notes=request.POST['Description'], timelineCheck="b")
        timelineObj.save()

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        redisNotiObj = {}
        redisNotiArr = []
        redisNotiObj["Notify"] = "%s"%request.user
        redisNotiObj["Message"] = "A new Bug was raised"
        redisNotiObj["Type"] = 2
        redisNotiObj["Link"] = "%s"%reverse('CreateBug')
        redisNotiArr.append(redisNotiObj)
        r.publish('chat', json.dumps(redisNotiObj))
        return HttpResponse("success")
    except Exception as ex:
        log.exception(ex)
        return HttpResponse(ex)

def upload_file(request):
    file = request.FILES['file']
    fileName = request.FILES['file'].name
    curUser = request.user
    newFileName = "%s_%s" % (curUser, fileName)
    handle_uploaded_file(file, newFileName)
    return HttpResponseRedirect(reverse('BugView'))


def handle_uploaded_file(f, FName):
    with open('D:/Work/Projects/Python/TeamTrack/BugTracker/BugScreenshotsTemp/%s' % FName, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def DeleteFileUploads(request):
    arr = request.POST.getlist('arr[]')
    curUser = request.user
    for item in arr:
        file_path = 'D:/Work/Projects/Python/TeamTrack/BugTracker/BugScreenshotsTemp/%s_%s' % (curUser, item)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as ex:
            return HttpResponse(ex)
    return HttpResponse("Success")
