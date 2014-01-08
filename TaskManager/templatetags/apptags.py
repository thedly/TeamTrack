from django import template
register = template.Library()
import datetime 

@register.filter    
def subtractDates(value):
    days = value - datetime.datetime.today().day
    if days > 5:
        return days
    elif days == 0:
        return "Last day to complete this task"
    elif days < 0:
        return "Task delayed"
    else:
        return "You only have %s days to complete the task"%days    
    return 