from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet
from TaskManager.models import *
from django.contrib.auth.models import User
from django.template import RequestContext
from TaskManager.forms import LoginForm,SearchForm,UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib import messages
import json
#import xlsxwriter
from django.conf.urls import include
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,FormView
from TaskManager.forms import LoginForm, SearchForm, MailForm, TimelineTaskUpdatesForm, CreateTaskForm, AddProjectForm, AddClientForm
from BugTracker.models import Bug
from django.contrib.auth.decorators import login_required
import win32com.client as pyCom
from django.conf import settings
import pythoncom
import redis
from django.core.mail import send_mail
import feedparser
from django.db.models import Count
from datetime import date, timedelta
#from reportlab.pdfgen import canvas
import datetime
import logging
log = logging.getLogger(__name__)

class LoginView(TemplateView):
    template_name = 'login.html'
    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['LoginForm'] = LoginForm()
        return context

class MeetingsView(TemplateView):
    template_name = 'meetings.html'

class CallView(TemplateView):
    template_name = 'Call.html'


class HomeView(TemplateView):
    
    template_name = 'home.html'
    log.debug("debug")
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['SearchForm'] = SearchForm()
        context['NoOfdays'] = datetime.datetime.now()
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        context['ip'] = ip
        TaskObj =  Tasks.objects.filter(Developer=self.request.user.id)
        context['inv'] = sum(p.Status.status == "Investigation" for p in TaskObj)
        context['dev'] = sum(p.Status.status == "Development" for p in TaskObj)
        context['test'] = sum(p.Status.status == "testing/bug fixing" for p in TaskObj)
        context['dep'] = sum(p.Status.status == "deployment" for p in TaskObj)
        context['tasksPending'] = TaskObj
        context['new'] = TaskmanagerTasktimeline.objects.filter(timelineCheck="").annotate(sco=Count('taskid')).count()
        context['bug'] = Bug.objects.all().count()
        d=date.today()-timedelta(days=7)

        context['timelineObj'] =  TaskmanagerTasktimeline.objects.filter(date__gte=d ,owner=self.request.user.id).order_by('-date')
        return context

class MailView(FormView):
    
    template_name = 'MailTemplate.html'
    form_class = MailForm

    def get_context_data(self, **kwargs):
        context = super(MailView, self).get_context_data(**kwargs)
        context['theme'] = self.request.session['userTheme']
        return context
    # def form_valid(self, form):
    #     form.send_email()
    #     return super(MailView,self).form_valid(form)
    # def get_context_data(self, **kwargs):
    #     context = super(MailView, self).get_context_data(**kwargs)
    #     pythoncom.CoInitialize()
    #     outlook = pyCom.Dispatch("Outlook.Application")
    #     namespace = outlook.GetNamespace("MAPI")
    #     inbox  = namespace.GetDefaultFolder(6)
    #     messages = inbox.Items
    #     context['inboxMsgs'] = messages
    #     return context
    

class TaskTypeView(TemplateView):
    template_name = 'taskTypeView.html'

    def get_context_data(self, **kwargs):
        TaskObj =  Tasks.objects.filter(Developer=self.request.user.id)
        context = super(TaskTypeView, self).get_context_data(**kwargs)
        context['inv'] = sum(p.Status.status == "Investigation" for p in TaskObj)
        context['dev'] = sum(p.Status.status == "Development" for p in TaskObj)
        context['test'] = sum(p.Status.status == "testing/bug fixing" for p in TaskObj)
        context['dep'] = sum(p.Status.status == "deployment" for p in TaskObj)
        context['new'] = TaskmanagerTasktimeline.objects.filter(timelineCheck="").annotate(sco=Count('taskid')).count()
        context['bug'] = Bug.objects.all().count()

        type = self.request.GET['type']

        if type == "new":
            taskObj = TaskmanagerTasktimeline.objects.filter(timelineCheck="").annotate(sco=Count('taskid'))
        elif type == "bug":
            taskObj = Bug.objects.all()
        elif int(type) > 4:
            type = None
            taskObj = None
        else:
            taskObj = Tasks.objects.filter(Status=type)


        context['tasks'] = taskObj
        context['type'] = type
        return context

class ProjectsView(TemplateView):
    template_name = 'Projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsView, self).get_context_data(**kwargs)
        context['Projects'] = Projects.objects.all()
        context['AddProjectForm'] = AddProjectForm()
        context['AddClientForm'] = AddClientForm()
        return context
    
class OngoingProjectsView(ListView):
    template_name = 'ongoingprojects.html'
    queryset = Projects.objects.filter(IsCompleted=False)
    

class CompletedProjectsView(ListView):
    template_name = 'completedprojects.html'
    queryset = Projects.objects.filter(IsCompleted=True)



class ProjectsDetailView(DetailView):
    model = Projects
    template_name = 'ProjectsDetail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsDetailView, self).get_context_data(**kwargs)
        context['Tasks'] = Tasks.objects.filter(ProjectId=self.kwargs['pk'])
        context['Timeline'] = TaskmanagerTasktimeline.objects.filter(project=self.kwargs['pk']).order_by('-date')
        feed = feedparser.parse('https://bitbucket.org/anuppadmanabha/saaramsha-v1/rss?token=0d36719c29b83c792781922ecbfb26bb')
        context['entries'] = feed['entries']
        return context

class ProjectsListView(ListView):
    model = Tasks
    template_name = 'Projectslist.html'
    context_object_name = "Projects_list"

class ProjectsCreate(CreateView):
    model = Projects
    template_name='CreateProjects.html'

class AddClientView(CreateView):
    model = Client
    template_name = 'AddClient.html'
    
    
class TasksView(ListView):
    template_name = 'Tasks.html'
    context_object_name = "Tasks"
    queryset = Tasks.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TasksView, self).get_context_data(**kwargs)
        context['CreateTaskForm'] = CreateTaskForm()
        return context

class TasksDetailView(DetailView):
    model = Tasks
    template_name = 'tasksDetail.html'
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.publish('chat', "Redis notification : Timeline event was created")
    def get_context_data(self, **kwargs):
        context = super(TasksDetailView, self).get_context_data(**kwargs)
        context['TimelineTaskUpdatesForm'] = TimelineTaskUpdatesForm()
        context['Timeline'] = TaskmanagerTasktimeline.objects.filter(taskid=self.kwargs['pk']).order_by('-date')
        return context

    def form_valid(self, form):
        log.debug('TasksDetailView')
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
    
class TasksUpdateView(UpdateView):
    model = Tasks
    template_name = 'tasksDetail.html'
    context_object_name = "Tasks_update"
    
    def get_context_data(self, **kwargs):
        context = super(TasksUpdateView, self).get_context_data(**kwargs)
        context['TaskTrack'] = TaskTrack.objects.filter(taskid=self.kwargs['pk'])
        return context


class TasksListView(ListView):
    model = Tasks
    template_name = 'taskdetail.html'
    context_object_name = "Tasks_detail"


class TasksCreate(CreateView):
    model = Tasks
    template_name='CreateTasks.html'




class ProfileView(ListView):
    model = ExtendedUser
    template_name = 'profileslist.html'
    context_object_name = "Profiles_list"

class CreateProfileView(CreateView):
    model = ExtendedUser
    template_name = 'Createprofile.html'
    form_class = UserCreationForm

class ProfileDetailView(DetailView):
    model = User
    template_name = 'profileDetail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['DevelopersTask'] = Tasks.objects.filter(Developer=self.kwargs['pk'])
        context['userDetails'] = ExtendedUser.objects.get(pk=self.kwargs['pk'])
        return context

def CreateMeetingRequest(request):
    pythoncom.CoInitialize()
    # outlook = pyCom.Dispatch("Outlook.Application")
    # namespace = outlook.GetNamespace("MAPI")
    # appointments = namespace.GetDefaultFolder(9).Items
    # #appointments.Sort("[Start]")
    # #appointments.IncludeRecurrences = "True"
    # appointment = appointments.GetFirst()
    oOutlook = pyCom.Dispatch("Outlook.Application")
    appt = oOutlook.CreateItem(1) # 1 - olAppointmentItem
    appt.Start = '2014-02-10 7:00'
    appt.Subject = 'Follow Up Meeting'
    appt.Duration = 15
    appt.Location = 'Office - Room 132A'
    appt.MeetingStatus = 1 # 1 - olMeeting; Changing the appointment to meeting
    #only after changing the meeting status recipients can be added
    appt.Recipients.Add("tejashedly@achumen.com")
    appt.Save()
    appt.Send()
    return HttpResponse("success")

class CalenderView(TemplateView):
    template_name='calender.html'

class UpdatesDetailView(TemplateView):
    template_name='updatesDetail.html'
    
    def get_context_data(self, **kwargs):
        context = super(UpdatesDetailView, self).get_context_data(**kwargs)
        context['WeeklyUpdates'] = WeeklyUpdates.objects.filter(owner=self.kwargs['pk'])
        return context    
    
def SearchResults(request):
    searchform = SearchForm()
    sqs = SearchQuerySet().models(User,Projects,Tasks).load_all().auto_query(request.GET['Search'])
    return render_to_response('searchresults.html',{'object_list':sqs,'searchform':searchform},RequestContext(request))

def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="C:/Users/tejas/Desktop/Kivy-latest.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    #p.save()
    return response
    

def authenticateUser(request):
    filled_form = LoginForm(request.POST)
    if filled_form.is_valid():
        customerEmail = request.POST['Username']
        customerPassword = request.POST['Password']
        user = authenticate(username=customerEmail, password=customerPassword)
        if user is not None:   
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.POST['next'])
            else:
                messages.add_message(request, messages.ERROR, 'The user has been Disabled.please contact the administrator')
                return HttpResponseRedirect(reverse('loginpage'))
        else:
            messages.add_message(request, messages.ERROR, 'The User does not exist')
            return HttpResponseRedirect(reverse('loginpage'))
    else:
        return HttpResponse('form not valid')

def userlogout(request):
    logout(request)
    cache.clear()
    messages.add_message(request, messages.INFO, "You have successfully logged out")
    return HttpResponseRedirect(reverse('loginpage'))
    
# def GenerateTimesheet(request):
#     workbook = xlsxwriter.Workbook('demo.xlsx')
#     worksheet = workbook.add_worksheet()
#     # Widen the first column to make the text clearer.
#     worksheet.set_column('A:A', 3)
#     worksheet.set_column('B:B', 47)
#     worksheet.set_column('C:K', 5)
#     # Add a bg_color format to use to highlight cells.
#     bg_color = workbook.add_format({'bg_color':'#a6caf0'})
#     # Write some simple text.
#
#
#     for row in range(11, 14):
#         for col in range(0, 14):
#             worksheet.write(row, col, '',bg_color)
#     i = 1
#     for row in range(14, 32):
#         for col in range(0, 14):
#             if col == 0:
#                 worksheet.write(row, 0, i ,bg_color)
#                 i = i + 1
#             elif col == 9 or col == 10:
#                 worksheet.write(row, col, '',bg_color)
#             else:
#                 worksheet.write(row,'', '',bg_color)
#     for col in range(0, 14):
#         worksheet.write(32, col, '',bg_color)
#
#     worksheet.write(32, col, '',bg_color)
#     worksheet.write(12, 0, 'No.',bg_color)
#     worksheet.write(12, 1, 'Task Description.',bg_color)
#     worksheet.write(11, 2, 'Start Time.',bg_color)
#     worksheet.write(12, 2, 'End Time.',bg_color)
#     worksheet.write(13, 2, 'Hours.',bg_color)
#
#     worksheet.write(13, 3, 'Mon',bg_color)
#     worksheet.write(13, 4, 'Tue',bg_color)
#     worksheet.write(13, 5, 'Wed',bg_color)
#     worksheet.write(13, 6, 'Thu',bg_color)
#     worksheet.write(13, 7, 'Fri',bg_color)
#     worksheet.write(13, 8, 'Sat',bg_color)
#
#
#     #worksheet.set_row(12,20, bg_color)
#     # Write some numbers, with row/column notation.
#
#     # Insert an image.
#     worksheet.insert_image('A0', '/var/www/my_eclipse_workspace/TeamTrack/TaskManager/static/images/achumenTimesheet.png')
#     workbook.close()
#     return HttpResponse(workbook)


# def view_event_request(request):
#     return HttpResponse("hi", mimetype='text/event-stream')

def CreateTimelineEvent(request):
    #if request.method == 'POST':
    try:
        log.debug("received taskId : %s"%request.POST['taskid'])
        obj = Tasks.objects.get(pk=request.POST['taskid'])

        obj.Status = TaskStatus.objects.get(pk=request.POST['status'])
        log.debug("received status : %s"%request.POST['status'])

        obj.save()
        log.debug("Object updated")
        timelineObj = TaskmanagerTasktimeline(project=obj.ProjectId, title=request.POST['Title'],  taskid=obj, status=obj.Status, owner=obj.Owner, notes=request.POST['notes'])
        if TaskmanagerTasktimeline.objects.all():
            TimelineInstance = TaskmanagerTasktimeline.objects.latest('date')
            if TimelineInstance.status == obj.Status:
                timelineObj.timelineCheck = "u"
            else:
                timelineObj.timelineCheck = "c"
        else:
            timelineObj.timelineCheck = "c"

        timelineObj.save()
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        redisNotiObj = {}
        redisNotiArr = []
        redisNotiObj["Notify"] = "%s"%request.user
        redisNotiObj["Message"] = "Timeline event was created"
        redisNotiObj["Type"] = 2
        redisNotiObj["Link"] = "%s#TimeLineEvents"%reverse('tasksdetail', kwargs={'pk': obj.id})
        redisNotiArr.append(redisNotiObj)
        r.publish('chat', json.dumps(redisNotiObj))
        return HttpResponse("success")#Redirect(reverse('tasksdetail', args=(request.POST['taskid'],)))
    except Exception as e:
        log.exception(e.message)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        redisNotiObj = {}
        redisNotiArr = []
        redisNotiObj["Notify"] = "%s"%request.user
        redisNotiObj["Message"] = "Something went terribly wrong ! Our developers are looking into it. Please try again until then."
        redisNotiObj["Type"] = 2
        redisNotiObj["Link"] = "#"
        redisNotiArr.append(redisNotiObj)
        r.publish('chat', json.dumps(redisNotiObj))
        return HttpResponse("failed")
    #else:
     #   return HttpResponseRedirect(reverse('tasksdetail', args=(taskid,))) # Redirect after POST


def chatMessage(request):
    # try:
    msg = request.GET['Message']
    notify = request.GET['Notify']
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    redisNotiObj = {}
    redisNotiObj["Notify"] = notify
    redisNotiObj["Message"] = msg
    redisNotiObj["Type"] = 1
    redisNotiObj["From"] = "%s" % request.user
    r.publish('chat', json.dumps(redisNotiObj))
    return HttpResponse("success")
    # except Exception as ex:
    #     r = redis.StrictRedis(host='localhost', port=6379, db=0)
    #     redisNotiObj = {}
    #     redisNotiArr = []
    #     redisNotiObj["Notify"] = "%s"%request.user
    #     redisNotiObj["Message"] = "Something went terribly wrong ! Our developers are looking into it. Please try again until then."
    #     redisNotiObj["Type"] = 2
    #     redisNotiObj["Link"] = "#"
    #     redisNotiArr.append(redisNotiObj)
    #     r.publish('chat', json.dumps(redisNotiObj))
    #     return HttpResponse("failed")

def CreateTask(request):
    try:
        log.debug("project id : %s , TaskTitle : %s , Description : %s "%(request.POST['ProjectId'], request.POST['TaskTitle'],request.POST['Description'] ))
        obj = Tasks(ProjectId=Projects.objects.get(pk=request.POST['ProjectId']), TaskTitle=request.POST['TaskTitle'], Description=request.POST['Description'], Requirement=request.POST['Requirement'], Owner=ExtendedUser.objects.get(pk=request.POST['UserId']), Developer=ExtendedUser.objects.get(pk=request.POST['UserId']), EndDate=request.POST['EndDate'], StartDate=datetime.datetime.now())
        obj.Status = TaskStatus.objects.get(pk=1) # creating task so status is 1
        obj.save()
        timelineObj = TaskmanagerTasktimeline(project=Projects.objects.get(pk=request.POST['ProjectId']), title=request.POST['TaskTitle'], taskid=Tasks.objects.get(pk=obj.id), status=obj.Status, owner=ExtendedUser.objects.get(pk=obj.Owner), notes="Task started")
        timelineObj.save()

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        redisNotiObj = {}
        redisNotiArr = []
        redisNotiObj["Notify"] = "%s"%request.user
        redisNotiObj["Message"] = "A new task was created"
        redisNotiObj["Type"] = 2
        redisNotiObj["Link"] = "%s"%reverse('tasksdetail', kwargs={'pk': obj.id})
        redisNotiArr.append(redisNotiObj)
        r.publish('chat', json.dumps(redisNotiObj))

        return HttpResponse("success")
    except Exception as ex:
        return HttpResponse(ex.message)

class ChatRoom(TemplateView):
    template_name = 'ChatRoom.html'

def SendMail(request):
    MessageEmailList = request.POST['MessageEmailList']
    MessageSubject = request.POST['MessageSubject']
    MessageText = request.POST['MessageText']
    send_mail(MessageSubject, MessageText, "tj.werewolf@gmail.com", MessageEmailList.split(","))
    return HttpResponse("success")

def ChangeTheme(request):
    try:
        themeToBeApplied = request.POST['themeToBeApplied']
        ExtendedUser.objects.filter(pk=request.user.id).update(theme=themeToBeApplied)
        del request.session['userTheme']
        log.debug("success")
        return HttpResponse("success")

    except Exception as ex:
        log.exception(ex)
        return HttpResponse(ex.message)

def getTaskStatus(request):
    try:
        statusId = request.GET['status']
        return HttpResponse(statusId.split('_')[0])
        if statusId.index('_') :
            tasks = TaskmanagerTasktimeline.objects.filter(status = statusId)
        else:
            tasks = TaskmanagerTasktimeline.objects.filter(status = statusId.split('_')[0], timelineCheck = statusId.split('_')[1].split('/')[0])
        log.debug("success")
        return render_to_response("TaskStatus.html", tasks)

    except Exception as ex:
        log.exception(ex)
        return HttpResponse(ex.message)

def getRSSFeed(request):

    return HttpResponse("hi")

def setSessionMap(request):
    try:
        lat = request.POST['lat']
        lon = request.POST['lon']
        ExtendedUser.objects.filter(pk=request.user.id).update(lastloggedinform=lat+"|"+lon)
        if 'lat' not in request.session:
            request.session['lat'] = lat
            request.session['lon'] = lon
        else:
            pass
        return HttpResponse("success")
    except Exception as ex:
        log.exception(ex)
        return HttpResponse(ex.message)