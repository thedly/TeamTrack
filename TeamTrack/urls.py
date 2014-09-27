from django.conf.urls import patterns, include, url
from tastypie.api import Api

from Services import *


v1_api = Api(api_name='v1')
v1_api.register(TasksResource())
v1_api.register(UserResource())
v1_api.register(ProjectsResource())
v1_api.register(LeavesResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def if_installed(appname, *args, **kwargs):
    import settings
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    # url(r'^TaskManager/', include('TaskManager.urls')),
    # url(r'^LeaveManager/', include('LeaveManager.urls')),
    # url(r'^BugTracker/', include('BugTracker.urls')),
    if_installed('TaskManager', r'^TaskManager/', include('TaskManager.urls')),
    if_installed('LeaveManager', r'^LeaveManager/', include('LeaveManager.urls')),
    if_installed('BugTracker', r'^BugTracker/', include('BugTracker.urls')),
)


    # AppsList = []
    # with open(os.path.abspath("TaskManager/static/Config/Applications.json")) as f:
    #     jsonContent = json.load(f)
    #     for item in jsonContent["Apps"]:
    #         AppsList.append(item)
    # patterns('')
    # TeamTrack += tuple(AppsList)
    # settings.INSTALLED_APPS += tuple(AppsList)

