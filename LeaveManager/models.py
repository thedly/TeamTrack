from django.db import models
from TaskManager.models import ExtendedUser


# Create your models here.
class LeavemanagerLeaves(models.Model):
    Id = models.IntegerField(primary_key=True, db_column='Id') # Field name made lowercase.
    Purpose = models.CharField(max_length=200L, db_column='Purpose') # Field name made lowercase.
    StartDate = models.DateTimeField(db_column='StartDate') # Field name made lowercase.
    EndDate = models.DateTimeField(db_column='EndDate') # Field name made lowercase.
    UserId = models.ForeignKey(ExtendedUser, db_column='UserId') # Field name made lowercase.
    emergencyleave = models.BooleanField(db_column='EmergencyLeave') # Field name made lowercase.
    approved = models.BooleanField(db_column='Approved') # Field name made lowercase.
    class Meta:
        db_table = 'leavemanager_leaves'

