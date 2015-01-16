from django.db import models
from TaskManager.models import ExtendedUser, Tasks
from django.contrib.auth.models import User
# Create your models here.

class Bug(models.Model):
    title = models.CharField(max_length=150)
    taskid = models.ForeignKey(Tasks, db_column='TaskId') # Field name made lowercase.
    description = models.TextField()
    status = models.CharField(max_length=50)
    owner = models.ForeignKey(ExtendedUser)
    def __unicode__(self):
        return "%s" % self.title

class BugScreenShots(models.Model):
    imageId = models.ForeignKey(Bug, db_column='imageId')
    imageName = models.CharField(max_length=50)
    imagePath = models.CharField(max_length=350)
    CreateDate = models.DateTimeField()
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.imageName

class BugComments(models.Model):
    CommentId = models.ForeignKey(Bug)
    Comment = models.TextField()
    def __unicode__(self):
        return "%s"%self.CommentId