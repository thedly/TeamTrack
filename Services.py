from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from TaskManager.models import Tasks, Projects, TaskStatus
from LeaveManager.models import LeavemanagerLeaves
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.utils import trailing_slash
from django.conf.urls import url
import logging
log = logging.getLogger(__name__)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        fields = ('username','id')

class ProjectsResource(ModelResource):
    class Meta:
        queryset = Projects.objects.all()
        resource_name = 'projects'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()

class StatusResource(ModelResource):
    class Meta:
        queryset = TaskStatus.objects.all()
        resource_name = 'Status'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()

class LeavesResource(ModelResource):
    UserId = fields.ForeignKey(UserResource, 'UserId') # Field name made lowercase.
    class Meta:
        queryset = LeavemanagerLeaves.objects.all()
        resource_name = 'leaves'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        cache = SimpleCache(timeout=10)

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/(?P<pk>\d+)/ApproveLeave%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ApproveLeave'), name='api_ApproveLeave'),
            url(r'^(?P<resource_name>%s)/(?P<pk>\d+)/RejectLeave%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('RejectLeave'), name='api_RejectLeave'),
        ]

    def ApproveLeave(self, request, **kwargs):
        response = ""
        log.debug("Approve leave method called")
        try:
            LeaveObj = LeavemanagerLeaves.objects.get(pk=kwargs['pk'])
            LeaveObj.approved = True
            LeaveObj.save()
            response = "success"
        except Exception as ex:
            response = ex.message
        # using the primary key defined in the url, obtain the game

        # Return what the method output, tastypie will handle the serialization
        return self.create_response(request, response)

    def RejectLeave(self, request, **kwargs):
        log.debug("Reject leave method called")
        response = ""
        try:
            LeaveObj = LeavemanagerLeaves.objects.get(pk=kwargs['pk'])
            LeaveObj.approved = False
            LeaveObj.save()
            response = "success"

        except Exception as ex:
            response = ex.message
        # using the primary key defined in the url, obtain the game

        # Return what the method output, tastypie will handle the serialization
        return self.create_response(request, response)

class TasksResource(ModelResource):
    ProjectId = fields.ForeignKey(ProjectsResource,'ProjectId')
    Owner = fields.ForeignKey(UserResource,'Owner')
    Developer = fields.ForeignKey(UserResource,'Developer')
    Status = fields.ForeignKey(StatusResource,'Status')
    class Meta:
        queryset = Tasks.objects.all()
        resource_name = 'tasks'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        filtering = {'id':ALL}
        
        
        
        