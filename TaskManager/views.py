from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet
from TaskManager.models import Projects,Tasks,TaskTrack
from django.contrib.auth.models import User
from django.template import RequestContext
from TaskManager.forms import LoginForm,SearchForm
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib import messages
import xlsxwriter
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView
from TaskManager.forms import UpdatesForTodayForm,LoginForm,SearchForm,MailForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage,send_mass_mail
import logging
log = logging.getLogger(__name__)

class LoginView(TemplateView):
    template_name = 'login.html'
    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['LoginForm'] = LoginForm()
        return context

class HomeView(TemplateView):
    
    template_name = 'home.html'
    log.debug("debug")
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        
        context['SearchForm'] = SearchForm()
        return context

class MailView(TemplateView):
    
    template_name = 'MailTemplate.html'
    success_url = '/sendMail/'
    
    def form_valid(self, form):
        message = EmailMessage(subject=form.Subject,
                       body=form.Message,
                       from_email=form.sender,
                       to=form.to_addresses,
                       bcc=form.cc_addresses,
                       headers={'Cc': ','.join(form.cc_addresses)})
        message.send()
        datatuple = (
            ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
            ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
        )
        send_mass_mail(datatuple)


        return super(MailView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(MailView, self).get_context_data(**kwargs)
        context['MailForm'] = MailForm()
        context['Users'] = User.objects.all()
        return context

class ProjectsView(TemplateView):
    template_name = 'Projects.html'
    
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
        return context
    
class ProjectsListView(ListView):
    model = Tasks
    template_name = 'Projectslist.html'
    context_object_name = "Projects_list"

class ProjectsCreate(CreateView):
    model = Projects
    template_name='CreateProjects.html'


class TasksView(TemplateView):
    template_name = 'Tasks.html'

class TasksDetailView(DetailView):
    model = Tasks
    template_name = 'taskdetail.html'
    context_object_name = "Tasks_detail"
    
    def get_context_data(self, **kwargs):
        context = super(TasksDetailView, self).get_context_data(**kwargs)
        context['TaskTrack'] = TaskTrack.objects.filter(taskid=self.kwargs['pk'])
        return context

class TasksUpdateView(UpdateView):
    model = Tasks
    template_name = 'tasksEdit.html'
    context_object_name = "Tasks_update"

class TasksListView(ListView):
    model = Tasks
    template_name = 'taskdetail.html'
    context_object_name = "Tasks_detail"

class TasksCreate(CreateView):
    model = Tasks
    template_name='CreateTasks.html'


class ProfileView(ListView):
    model = User
    template_name = 'profileslist.html'
    context_object_name = "Profiles_list"

class ProfileDetailView(DetailView):
    model = User
    template_name = 'profileslistdetail.html'
    context_object_name = "Profiles_detail"

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['DevelopersTask'] = Tasks.objects.filter(Developer=self.kwargs['pk'])
        context['DesignersTask'] = Tasks.objects.filter(Designer=self.kwargs['pk'])
        return context

def SearchResults(request):
    searchform = SearchForm()
    sqs = SearchQuerySet().models(User,Projects,Tasks).load_all().auto_query(request.GET['Search'])
    return render_to_response('searchresults.html',{'object_list':sqs,'searchform':searchform},RequestContext(request))


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
    
def GenerateTimesheet(request):
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet()
    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:B', 47)
    worksheet.set_column('C:K', 5)
    # Add a bg_color format to use to highlight cells.
    bg_color = workbook.add_format({'bg_color':'#a6caf0'})
    # Write some simple text.
    
    
    for row in range(11, 14):
        for col in range(0, 14):
            worksheet.write(row, col, '',bg_color)
    i = 1
    for row in range(14, 32):
        for col in range(0, 14):
            if col == 0:
                worksheet.write(row, 0, i ,bg_color)
                i = i + 1
            elif col == 9 or col == 10:
                worksheet.write(row, col, '',bg_color)
            else:
                worksheet.write(row,'', '',bg_color)
    for col in range(0, 14):
        worksheet.write(32, col, '',bg_color)
    
    worksheet.write(32, col, '',bg_color)
    worksheet.write(12, 0, 'No.',bg_color)
    worksheet.write(12, 1, 'Task Description.',bg_color)
    worksheet.write(11, 2, 'Start Time.',bg_color)
    worksheet.write(12, 2, 'End Time.',bg_color)
    worksheet.write(13, 2, 'Hours.',bg_color)
    
    worksheet.write(13, 3, 'Mon',bg_color)
    worksheet.write(13, 4, 'Tue',bg_color)
    worksheet.write(13, 5, 'Wed',bg_color)
    worksheet.write(13, 6, 'Thu',bg_color)
    worksheet.write(13, 7, 'Fri',bg_color)
    worksheet.write(13, 8, 'Sat',bg_color)
    
    
    #worksheet.set_row(12,20, bg_color)
    # Write some numbers, with row/column notation.
    
    # Insert an image.
    worksheet.insert_image('A0', '/var/www/my_eclipse_workspace/TeamTrack/TaskManager/static/images/achumenTimesheet.png')
    workbook.close()
    return HttpResponse(workbook) 