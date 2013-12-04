from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Projects(models.Model):
    Title = models.CharField(max_length=100)
    IsCompleted = models.BooleanField(default=False)
    StartDate = models.DateField(auto_now=True)
    EndDate = models.DateField()
    
    def __unicode__(self):
        return "%s"%self.Title
    
    @models.permalink
    def get_absolute_url(self):
        return ('projectsdetail', [self.id])

class TaskStatus(models.Model):
    status = models.CharField(max_length=150,default="initiated")
    
    def __unicode__(self):
        return self.status
    
class Tasks(models.Model):
    ProjectId = models.ForeignKey(Projects)
    TaskTitle = models.CharField(max_length=100)
    Description = models.TextField()
    Requirement = models.TextField()
    Owner = models.ForeignKey(User,related_name='Owner')
    Designer = models.ForeignKey(User,related_name='Designer')
    Developer = models.ForeignKey(User,related_name='Developer')
    Status = models.ForeignKey(TaskStatus)
    StartDate = models.DateField(auto_now=True)
    EndDate = models.DateField()
    
    def __unicode__(self):
        return self.TaskTitle
    
    @models.permalink
    def get_absolute_url(self):
        return ('taskdetail', [self.id])
    



class TaskTrack(models.Model):
    project = models.ForeignKey(Projects)
    taskid = models.ForeignKey(Tasks)
    status = models.ForeignKey(TaskStatus)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.status
            
            
class WeeklyUpdates(models.Model):
    project = models.ForeignKey(Projects)
    taskid = models.ForeignKey(Tasks)
    status = models.ForeignKey(TaskStatus)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.status