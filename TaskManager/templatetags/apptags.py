from django import template
register = template.Library()
import datetime
from django.http import HttpResponse

@register.filter    
def subtractDates(value):
    SubtractedDate = value - datetime.datetime.today().date()
    days = SubtractedDate.days
    if days > 5:
        return "%s days left"%days
    elif days == 0:
        return "Last day"
    elif days < 0:
        return "Task delayed"
    else:
        return "only %s days left"%days
    return

@register.filter
def TaskPercentage(TaskDate, ProjectDate):
    ProjectDate_days = ProjectDate.date.days
    TaskDate_days = TaskDate.date.days
    percentValue = (TaskDate_days/ProjectDate_days)*100
    return percentValue+"%"