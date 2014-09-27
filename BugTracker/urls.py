from django.conf.urls import url, patterns
from BugTracker.views import *

urlpatterns = patterns('',
    url('^$',  BugView.as_view(),name='BugView'),
    url('^CreateBug/$','BugTracker.views.RaiseABug', name='CreateBug'),
    url('^UploadImages/$',  'BugTracker.views.upload_file' ,name='UploadImages'),
    url('^DeleteFileUploads/$',  'BugTracker.views.DeleteFileUploads' ,name='DeleteFileUploads'),



)