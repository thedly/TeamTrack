from haystack import indexes
from django.contrib.auth.models import User
from TaskManager.models import Projects,Tasks

class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model=User
    
    def index_queryset(self, using=None):
        return User.objects.all()

class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model=Projects
    
    def index_queryset(self, using=None):
        return Projects.objects.all()
    
class TaskIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model=Tasks
    
    def index_queryset(self, using=None):
        return Tasks.objects.all()