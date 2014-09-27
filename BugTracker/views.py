# Create your views here.
from django.views.generic.base import TemplateView
from BugTracker.forms import CreateBugForm
from BugTracker.models import Bug
from TaskManager.models import Tasks, TaskStatus, TaskmanagerTasktimeline, ExtendedUser
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime
from TeamTrack.settings import STATIC_URL
import logging
import os
import json
log = logging.getLogger(__name__)
from mimetypes import MimeTypes

class BugView(TemplateView):
    template_name = "bugs.html"

    def get_context_data(self, **kwargs):
        context = super(BugView, self).get_context_data(**kwargs)
        context['BugForm'] = CreateBugForm()
        context['Bugs'] = Tasks.objects.filter(Status=3)
        return context

def RaiseABug(request):
    obj = Tasks.objects.get(pk=request.POST['TaskId'])
    obj.Status = TaskStatus.objects.get(pk=3)
    obj.save()
    project = obj.ProjectId
    timelineObj = TaskmanagerTasktimeline(project=project, taskid=obj, status=obj.Status, owner=ExtendedUser.objects.get(pk=request.user.id), notes="A bug has been raised", timelineCheck="b")
    timelineObj.save()
    return HttpResponseRedirect(reverse('BugView'))


def upload_file(request):
    log.debug("Entered the upload file method")
    file = request.FILES['file']
    fileName = request.FILES['file'].name
    fileType = request.FILES['file'].content_type
    handle_uploaded_file(file, fileName, fileType)
    log.debug("Finished handle upload file method, redirecting")
    return HttpResponseRedirect(reverse('BugView'))


def handle_uploaded_file(f, FName, FType):
    if FType is None:
        FType = "application/text"
    fName = FName.split('.')[0]
    fType = FType.split('/')[1]

    log.debug("handle upload file method called")
    log.debug("%s %s"% (FName, FType))
    with open('D:/Work/Projects/Python/TeamTrack/TaskManager/static/images/%s.%s' % (fName, fType), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def DeleteFileUploads(request):
    arr = request.POST.getlist('arr[]')
    for item in arr:
        file_path = 'D:/Work/Projects/Python/TeamTrack/TaskManager/static/images/%s' % item
        try:
            os.unlink(file_path)
        except Exception as ex:
            return HttpResponse(ex)
    return HttpResponse("Success")