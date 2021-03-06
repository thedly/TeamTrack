from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ExtendedUser(User):
    birthdate = models.DateField()
    rating = models.IntegerField()
    Machinename = models.CharField(db_column='MachineName', max_length=50) # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=100) # Field name made lowercase.
    theme = models.CharField(max_length=300)
    lastloggedinform = models.CharField(db_column='LastLoggedInForm', max_length=300) # Field name made lowercase.

    def __unicode__(self):
        return "%s"%self.username
    
    @models.permalink
    def get_absolute_url(self):
        return ('profileslistdetail',[self.id])

class Client(models.Model):
    Name = models.CharField(max_length=150)
    Email = models.EmailField()
    ContactNumber = models.BigIntegerField()
    AlternateContactNumber = models.BigIntegerField()
    
    def __unicode__(self):
        return "%s"%self.Name
    
    @models.permalink
    def get_absolute_url(self):
        return ('createprojects')

class Projects(models.Model):
    Title = models.CharField(max_length=100)
    IsCompleted = models.BooleanField(default=False)
    Client = models.ForeignKey(Client,default=1)
    StartDate = models.DateTimeField(auto_now=True)
    EndDate = models.DateTimeField()
    
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
    Owner = models.ForeignKey(ExtendedUser,related_name='Owner')
    Developer = models.ForeignKey(ExtendedUser,related_name='Developer')
    Status = models.ForeignKey(TaskStatus)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    modifieddate = models.DateTimeField(auto_now=True, db_column='ModifiedDate') # Field name made lowercase.
    
    def __unicode__(self):
        return self.TaskTitle
    
    @models.permalink
    def get_absolute_url(self):
        return ('taskdetail', [self.id])
    

class graphData(models.Model):
    taskid = models.ForeignKey(Tasks)
    proposedPlot = models.CharField(max_length=150) 
    processTPlot = models.CharField(max_length=150)

class TaskTrack(models.Model):
    project = models.ForeignKey(Projects)
    taskid = models.ForeignKey(Tasks)
    status = models.ForeignKey(TaskStatus)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(ExtendedUser)
    
    def __unicode__(self):
        return self.status
            
            
class WeeklyUpdates(models.Model):
    project = models.ForeignKey(Projects)
    taskid = models.ForeignKey(Tasks)
    status = models.ForeignKey(TaskStatus)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(ExtendedUser)
    notes = models.TextField(db_column='notes')
    
    def __unicode__(self):
        return self.notes

class TaskmanagerTasktimeline(models.Model):
    project = models.ForeignKey(Projects, db_column='project')
    taskid = models.ForeignKey(Tasks, db_column='taskid')
    status = models.ForeignKey(TaskStatus, db_column='status')
    title = models.CharField(db_column='Title', max_length=100)
    notes = models.TextField()
    owner = models.ForeignKey(ExtendedUser, db_column='owner')
    date = models.DateTimeField(auto_now=True)
    timelineCheck = models.CharField(max_length=20, db_column='timelineCheck')
    class Meta:
        db_table = 'taskmanager_tasktimeline'

    def __unicode__(self):
        return self.notes

class TeamtrackNotifications(models.Model):
    id = models.IntegerField(primary_key=True, db_column='Id')
    message = models.CharField(max_length=300L, db_column='Message')
    fromwhom = models.ForeignKey(ExtendedUser, db_column='FromWhom', related_name='FromWhom')
    towhom = models.ForeignKey(ExtendedUser, db_column='ToWhom', related_name='ToWhom')
    modelname = models.CharField(max_length=100L, db_column='ModelName') # Field name made lowercase.
    rowid = models.IntegerField(db_column='RowId') # Field name made lowercase.
    link = models.CharField(max_length=100L, db_column='Link')
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now=True)
    class Meta:
        db_table = 'teamtrack_notifications'
