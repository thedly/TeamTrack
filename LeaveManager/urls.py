from django.conf.urls import url, patterns
from LeaveManager.views import *
import TaskManager.Signals

urlpatterns = patterns('',
    url('^$',  HomeView.as_view(),name='LeaveManagerHome'),
    url('^SendLeaveRequest/$',  'LeaveManager.views.SendLeaveRequest', name='SendLeaveRequest'),

)