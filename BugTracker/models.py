from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BugScreenShots(models.Model):
    image = models.CharField(max_length=50)

class Bug(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    screenshots = models.ForeignKey(BugScreenShots)
    def __unicode__(self):
        return "%s"%self.title

class BugComments(models.Model):
    CommentId = models.ForeignKey(Bug)
    Comment = models.TextField()
    def __unicode__(self):
        return "%s"%self.CommentId