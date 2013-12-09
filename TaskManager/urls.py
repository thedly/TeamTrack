from django.conf.urls.defaults import patterns, include, url
#from django.views.generic.simple import direct_to_template
from TaskManager.models import Projects,Tasks
from TaskManager.views import LoginView,HomeView,ProjectsView,TasksView,TasksDetailView,TasksListView,TasksCreate,ProjectsCreate,ProfileView,TasksUpdateView,CalenderView
from TaskManager.views import ProjectsListView,ProjectsListView,ProjectsDetailView,MailView,OngoingProjectsView,CompletedProjectsView,ProfileDetailView,AddClientView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from TaskManager.forms import UpdatesForTodayForm,LoginForm,SearchForm
from haystack.query import SearchQuerySet
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView
from TaskManager import signals

urlpatterns = patterns('',

#-----------------Login----------------------------------------
    url('^$',  LoginView.as_view(),name='loginpage'),#direct_to_template, {'template': 'login.html','extra_context':{'LoginForm': LoginForm()}}, name="loginpage"),
    url('^authenticate/$', 'TaskManager.views.authenticateUser', name="authenticateuser"),
    url('^logout/$', 'TaskManager.views.userlogout', name="userlogout"),
#-----------------Projects--------------------------------------                       
    url('^projects/$', login_required(ProjectsView.as_view()), name="projects"),
    url('^CreateProject/$',ProjectsCreate.as_view(),name="createprojects"),
    url(r'^ProjectsList/$', ProjectsListView.as_view(), name='projectslist'),
    url('^projectsdetail/(?P<pk>\d+)/$', ProjectsDetailView.as_view(), name="projectsdetail"),
#-----------------Tasks--------------------------------------                       
    url('^tasks/$', login_required(TasksView.as_view()),name="tasks"),
    url('^CreateTask/$',login_required(TasksCreate.as_view()),name="createtasks"),
    url(r'^ProjectsList/$', login_required(TasksListView.as_view()), name='projectslist'),
    url('^taskdetail/(?P<pk>\d+)/$', login_required(TasksDetailView.as_view()), name="taskdetail"),
    url('^taskupdate/(?P<pk>\d+)/$', login_required(TasksUpdateView.as_view()), name="taskupdate"),

    
    url('^CalenderEvents/$', login_required(CalenderView.as_view()), name="CalenderEvents"),
    url('^GenerateTimeSheet/$','TaskManager.views.GenerateTimesheet',name='GenerateTimesheet'),
    url('^AddClient/$', login_required(AddClientView.as_view()), name="AddClient"),
    url('^mail/$', login_required(MailView.as_view()), name="mail"),
    url('^home/$', login_required(HomeView.as_view()),name='home'),#login_required(direct_to_template), {'template': 'home.html','login_required':True,'extra_context':{'SearchForm': SearchForm()}}, name="home"),
    url('^reports/$', login_required(TemplateView), {'template': 'reports.html'}, name="reports"),
    url('^ongoingprojects/$', OngoingProjectsView.as_view(),name="ongoingprojects"),
    url('^completedprojects/$', CompletedProjectsView.as_view(), name="completedprojects"),
    
    url('^profileslist/$', ProfileView.as_view(), {"queryset" : User.objects.all(),"template_name" : 'profileslist.html'} , name="profileslist"),
    url('^ViewResume/$','TaskManager.views.pdf_view',name='ViewResume'),
    url('^profileslistdetail/(?P<pk>\d+)/$', ProfileDetailView.as_view(), {"queryset" : User.objects.all(),"template_name" : 'profileslistdetail.html'} , name="profileslistdetail"),
    url('^updatesfortoday/$', TemplateView.as_view(), {'template': 'updatesfortoday.html','extra_context':{'UpdatesForTodayForm': UpdatesForTodayForm()}} , name="updatesfortoday"),
   
    url('^searchresults/$','TaskManager.views.SearchResults',name="searchresults"),
    url('^taskdetail/$', TemplateView.as_view(), {'template': 'taskdetail.html'}, name="taskdetail"),

    
)