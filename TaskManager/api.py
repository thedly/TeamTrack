from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from TaskManager.models import Tasks,Projects
from django.contrib.auth.models import User
from tastypie import fields

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

class TasksResource(ModelResource):
    ProjectId = fields.ForeignKey(ProjectsResource,'ProjectId')
    Owner = fields.ForeignKey(UserResource,'Owner')
    Designer = fields.ForeignKey(UserResource,'Designer')
    Developer = fields.ForeignKey(UserResource,'Developer')
    class Meta:
        queryset = Tasks.objects.all()
        resource_name = 'tasks'
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        filtering = {'id':ALL}
        
        
        
        