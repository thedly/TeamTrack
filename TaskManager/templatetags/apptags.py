from django import template
register = template.Library()
import datetime
from django.http import HttpResponse
from TaskManager.models import Tasks, Projects, TaskmanagerTasktimeline, ExtendedUser, TaskStatus, WeeklyUpdates
from LeaveManager.models import LeavemanagerLeaves
import json
import win32com.client as pyCom
import pythoncom
import logging
log = logging.getLogger(__name__)
from django.core.urlresolvers import reverse

@register.filter    
def subtractDates(value):
    log.debug("parameter : %s"%value)
    SubtractedDate = value - datetime.datetime.today().date()
    log.debug("SubtractedDate : %s"%SubtractedDate)
    days = SubtractedDate.days
    if days > 5:
        return "%s days left"%days
    elif days == 0:
        return "Last day"
    elif days < 0:
        return "Task delayed"
    else:
        return "only %s days left"%days

@register.filter
def AverageOfTaskStatus(value):
    TaskObj = Tasks.objects.filter(ProjectId=value)
    DataArray = []
    if TaskObj is None:
        return "-1"
    for Task in TaskObj:
        DataArray.append(int(Task.Status.id))
    return reduce(lambda x, y: x + y, DataArray) / len(DataArray)

@register.filter
def getEvents(value):
    LeavemanagerLeavesobj = LeavemanagerLeaves.objects.filter(UserId=ExtendedUser.objects.get(pk=value))
    arr = []
    for Leave in LeavemanagerLeavesobj:
        obj = {}
        obj["id"] = Leave.Id
        obj["start"] = Leave.StartDate.strftime('%Y-%m-%d')
        obj["title"] = Leave.Purpose
    arr.append(obj)
    return json.dumps(arr)

@register.simple_tag
def getDataIntoOptions(param):
    log.info(param)
    if param == "pro":
        ProjectObj = Projects.objects.all()
        str = "<option>No Filter</option>"
        for item in ProjectObj:
            newstr = "<option>%s</option>" % item.Title
            str = "%s%s" % (str, newstr)
        return str
    elif param == "tas":
        ProjectObj = Tasks.objects.all()
        str = "<option>No Filter</option>"
        for item in ProjectObj:
            newstr = "<option>%s</option>" % item.TaskTitle
            str = "%s%s" % (str, newstr)
        return str
    elif param == "sta":
        ProjectObj = TaskStatus.objects.all()
        str = "<option>No Filter</option>"
        for item in ProjectObj:
            newstr = "<option>%s</option>" % item.status
            str = "%s%s" % (str, newstr)
        return str
    elif param == "usr":
        ExtendedUserObj = ExtendedUser.objects.all()
        str = "<option>No Filter</option>"
        for item in ExtendedUserObj:
            newstr = "<option>%s</option>" % item.username
            str = "%s%s" % (str, newstr)
        return str

@register.simple_tag
def getLeaveEvents(id):
    LeaveObj = LeavemanagerLeaves.objects.filter(UserId=ExtendedUser.objects.get(pk=id))
    arrObj = []
    for Leave in LeaveObj:
        obj = {}
        obj["id"] = Leave.Id
        obj["start"] = Leave.StartDate.strftime("%Y-%m-%d")
        obj["title"] = Leave.Purpose
        if Leave.approved:
            obj["color"] = "#66CD00"

        arrObj.append(obj)
    return json.dumps(arrObj)

@register.simple_tag
def getProjects():
    ProjectObj = Projects.objects.all()
    proArr = []
    for pro in ProjectObj:
        proObj = {}
        proObj["title"] = pro.Title
        proObj["start"] = str(pro.StartDate.date())
        proObj["end"] = str(pro.EndDate.date())
        proObj["url"] = reverse("projectsdetail", kwargs={'pk': pro.id})
        proObj["editable"] = False
        proArr.append(proObj)
    return json.dumps(proArr)

@register.simple_tag
def getWeeklyUpdates():
    WeeklyUpdatesObj = WeeklyUpdates.objects.all()
    wupArr = []
    for wup in WeeklyUpdatesObj:
        wupObj = {}
        wupObj["title"] = wup.taskid.TaskTitle
        wupObj["start"] = wup.date
        wupObj["editable"] = False,
        #wupObj["url"] = reverse("taskdetail", kwargs={'pk': wup.taskid})
        wupArr.append(wupObj)
    return json.dumps(wupArr)

@register.simple_tag
def getMeetings():
    pythoncom.CoInitialize()
    outlook = pyCom.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    appointments = namespace.GetDefaultFolder(9).Items
    appointments.Sort("[Start]")
    appointments.IncludeRecurrences = "True"
    MeetingArr = []
    for appointment in appointments:
        MeetingObj = {}
        MeetingObj["title"] = appointment.Subject
        MeetingObj["start"] = str(datetime.date(appointment.Start.year, appointment.Start.month, appointment.Start.day))
        MeetingObj["editable"] = False,
        MeetingArr.append(MeetingObj)
    return json.dumps(MeetingArr)

@register.simple_tag
def getAddressBook():
    UserObj = ExtendedUser.objects.all()
    str = ""
    str += "<table class='EmailAddressBook'>"
    str += "<tr><th>Name</th><th>Email</th><th></th></tr>"
    for obj in UserObj:
        str += "<tr>"
        str += "<td>"+obj.username+"</td><td>"+obj.email+"</td>"
        str += "<td><input class='EmailAddressBookCheck' type='checkbox' value='"+obj.email+"'>"
        str += "</tr>"
    str += "</table>"
    return str;



@register.filter
def BuildDonutGraph(value):
    TaskObj = Tasks.objects.filter(ProjectId=value)
    ProjectObj = Projects.objects.get(pk=value)
    currentDate = datetime.datetime.today().date()
    ProjectEndDate = ProjectObj.EndDate
    ProjectSubtractDate = ProjectEndDate.date() - currentDate
    ProjectRemainingDays = ProjectSubtractDate.days
    DataArray = []
    TotalTaskDays = 0
    for task in TaskObj:
        DataObj = {}
        EndDate = task.EndDate
        subtractDates = EndDate.date() - currentDate
        TaskDaysRemaining = subtractDates.days
        TotalTaskDays = TotalTaskDays + TaskDaysRemaining
        log.debug("The remaining days for %s to end is %s"%(task, TaskDaysRemaining))
        log.debug("The remaining days for %s to end is %s"%(ProjectObj, ProjectRemainingDays))
        percentagePriority = round(((TaskDaysRemaining/(ProjectRemainingDays*1.0))*100), 2)
        log.debug("The division leads to %s"%percentagePriority)
        DataObj["label"] = str(task.TaskTitle)
        DataObj["value"] = str(percentagePriority)
        DataArray.append(DataObj)
    if ProjectRemainingDays > TotalTaskDays:
        DataObj = {}
        ExtraDays = ProjectRemainingDays - TotalTaskDays
        percDays = round(((ExtraDays/(ProjectRemainingDays*1.0))*100), 2)
        DataObj["label"] = "Extra time"
        DataObj["value"] = str(percDays)
        DataArray.append(DataObj)
    return json.dumps(DataArray)




@register.filter
def BuildLineGraph(value):
    TaskObj = Tasks.objects.get(pk=value)
    TaskmanagerTasktimelineObj = TaskmanagerTasktimeline.objects.filter(taskid=value)

    TaskStartDate = TaskObj.StartDate.date()
    TaskEndDate = TaskObj.EndDate.date()
    TaskSubtractDate = TaskEndDate - TaskStartDate
    TaskRemainingDays = TaskSubtractDate.days
    log.debug(TaskRemainingDays)
    DataArray = []
    TimelineDatesArray = []

    for tasktime in TaskmanagerTasktimelineObj:
        TimelineDatesArray.append(tasktime.date.date())
    log.debug("Timeline obj contains %s values"%TaskmanagerTasktimelineObj.count())
    log.debug("The events array is %s"%TimelineDatesArray)
    TotalTaskDays = 0
    InvPhaseDaysLim = int(round((0.15*TaskRemainingDays), 0))
    DevPhaseDaysLim = int(round((0.35*TaskRemainingDays), 0))
    TestPhaseDaysLim = int(round((0.80*TaskRemainingDays), 0))
    DeplPhaseDaysLim = int(round((1*TaskRemainingDays), 0))
    CurrentDate = datetime.datetime.today().date()
    log.debug("InvPhaseDaysLim : %s, DevPhaseDaysLim: %s, TestPhaseDaysLim: %s, DeplPhaseDaysLim: %s"%(InvPhaseDaysLim, DevPhaseDaysLim, TestPhaseDaysLim, DeplPhaseDaysLim))
    initialDate = TaskObj.StartDate
    StartDate = TaskObj.StartDate
    Modifieddate = TaskObj.modifieddate
    EndDate = TaskObj.EndDate
    DayCount = 1
    while StartDate <= EndDate:

        DataObj = {}
        DataObj['y'] = str(StartDate.date())
        log.debug("date : %s "%StartDate.date())
        log.debug("Current date : %s"%CurrentDate)
        log.debug("daycount : %s "%DayCount)
        if DayCount <= InvPhaseDaysLim:
            log.debug("investigation phase")
            log.debug((round((15*DayCount)/InvPhaseDaysLim, 1)))
            DataObj['a'] = (round((15*DayCount)/InvPhaseDaysLim, 1))
            if StartDate.date() >= CurrentDate:
                DataObj['b'] = 0
            else:
                if Modifieddate.date() in TimelineDatesArray:
                    NewStartDate = datetime.datetime.strptime(str(StartDate.date()), "%Y-%m-%d")
                    NewinitialDate = datetime.datetime.strptime(str(initialDate.date()), "%Y-%m-%d")
                    newDayCount = abs((NewStartDate - NewinitialDate).days)
                    log.debug("%s - %s = %s"%(NewStartDate, NewinitialDate, newDayCount))
                    log.debug("newDayCount : %s"%newDayCount)
                    #log.debug("newDayCount : %s "%str(newDayCount)
                    DataObj['b'] = (round((15*newDayCount)/InvPhaseDaysLim, 1))
                else:
                    log.debug("There was no update")
                    DataObj['b'] = 0 # there was no update
        elif DayCount <= DevPhaseDaysLim:
            log.debug("Development phase")
            log.debug((round((35*DayCount)/DevPhaseDaysLim, 1)))
            DataObj['a'] = (round((35*DayCount)/DevPhaseDaysLim, 1))
            if StartDate.date() >= CurrentDate:
                DataObj['b'] = 0
            else:
                if Modifieddate.date() in TimelineDatesArray:
                    NewStartDate = datetime.datetime.strptime(str(StartDate.date()), "%Y-%m-%d")
                    NewinitialDate = datetime.datetime.strptime(str(initialDate.date()), "%Y-%m-%d")
                    newDayCount = abs((NewStartDate - NewinitialDate).days)
                    log.debug("%s - %s = %s"%(NewStartDate, NewinitialDate, newDayCount))
                    log.debug("newDayCount : %s"%newDayCount)
                    DataObj['b'] = (round((15*newDayCount)/InvPhaseDaysLim, 1))
                else:
                    DataObj['b'] = 0 # there was no update
        elif DayCount <= TestPhaseDaysLim:
            log.debug("Testing phase")
            log.debug(int(round((80*DayCount)/TestPhaseDaysLim, 1)))
            DataObj['a'] = (round((80*DayCount)/TestPhaseDaysLim, 1))
            if StartDate.date() >= CurrentDate:
                DataObj['b'] = 0
            else:
                if Modifieddate.date() in TimelineDatesArray:
                    NewStartDate = datetime.datetime.strptime(str(StartDate.date()), "%Y-%m-%d")
                    NewinitialDate = datetime.datetime.strptime(str(initialDate.date()), "%Y-%m-%d")

                    newDayCount = abs((NewStartDate - NewinitialDate).days)
                    log.debug("%s - %s = %s"%(NewStartDate, NewinitialDate, newDayCount))
                    log.debug("newDayCount : %s"%newDayCount)
                    DataObj['b'] = (round((15*newDayCount)/InvPhaseDaysLim, 1))
                else:
                    DataObj['b'] = 0 # there was no update
        elif DayCount <= DeplPhaseDaysLim:
            log.debug("Deployment phase")
            log.debug((round((100*DayCount)/DeplPhaseDaysLim, 1)))
            DataObj['a'] = (round((100*DayCount)/DeplPhaseDaysLim, 1))
            if StartDate.date() >= CurrentDate:
                DataObj['b'] = 0
            else:
                if Modifieddate.date() in TimelineDatesArray:
                    NewStartDate = datetime.datetime.strptime(str(StartDate.date()), "%Y-%m-%d")
                    NewinitialDate = datetime.datetime.strptime(str(initialDate.date()), "%Y-%m-%d")
                    newDayCount = abs((NewStartDate - NewinitialDate).days)
                    log.debug("%s - %s = %s"%(NewStartDate, NewinitialDate, newDayCount))
                    log.debug("newDayCount : %s"%newDayCount)
                    DataObj['b'] = (round((15*newDayCount)/InvPhaseDaysLim, 1))
                else:
                    DataObj['b'] = 0 # there was no update
        log.debug("Current performance is %s" % (round((100*DayCount)/DeplPhaseDaysLim, 1)))
        DataArray.append(DataObj)
        DayCount = DayCount + 1
        StartDate = StartDate + datetime.timedelta(days=1)
    return json.dumps(DataArray)
