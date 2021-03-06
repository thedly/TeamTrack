from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template
from TaskManager.models import Projects,Tasks
from TaskManager.views import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from TaskManager.forms import *
from haystack.query import SearchQuerySet
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView


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
    #url('^CreateTask/$',login_required(TasksCreate.as_view()),name="createtasks"),
    url(r'^ProjectsList/$', login_required(TasksListView.as_view()), name='projectslist'),
    url('^taskupdate/(?P<pk>\d+)/$', login_required(TasksUpdateView.as_view()), name="taskupdate"),
    url('^CreateTask/$', 'TaskManager.views.CreateTask', name="CreateTask"),
    
    url('^Meetings/$', login_required(MeetingsView.as_view()), name="Meetings"),
    
    url('^CalenderEvents/$', login_required(CalenderView.as_view()), name="Events"),
    #url('^GenerateTimeSheet/$','TaskManager.views.GenerateTimesheet',name='GenerateTimesheet'),
    url('^AddClient/$', login_required(AddClientView.as_view()), name="AddClient"),
    url('^mail/$', login_required(MailView.as_view()), name="mail"),
    url('^home/$', login_required(HomeView.as_view()),name='home'),#login_required(direct_to_template), {'template': 'home.html','login_required':True,'extra_context':{'SearchForm': SearchForm()}}, name="home"),
    url('^reports/$', login_required(TemplateView), {'template': 'reports.html'}, name="reports"),
    url('^ongoingprojects/$', OngoingProjectsView.as_view(),name="ongoingprojects"),
    url('^completedprojects/$', CompletedProjectsView.as_view(), name="completedprojects"),
    
    url('^createprofile/$', login_required(CreateProfileView.as_view()), name="createprofile"),
    url('^profileslist/$', login_required(ProfileView.as_view()), name="profileslist"),
    url('^ViewResume/$','TaskManager.views.pdf_view',name='ViewResume'),
    url('^profileslistdetail/(?P<pk>\d+)/$', ProfileDetailView.as_view() , name="profilesdetail"),
    url('^userUpdates/(?P<pk>\d+)/$', UpdatesDetailView.as_view() , name="userUpdates"),
    url('^searchresults/$','TaskManager.views.SearchResults',name="searchresults"),
    url('^taskdetail/(?P<pk>\d+)/$', login_required(TasksDetailView.as_view()), name="tasksdetail"),
   url('^CreateTimelineEvent/$','TaskManager.views.CreateTimelineEvent',name='CreateTimelineEvent'),
      url('^ChatRoom/$', login_required(ChatRoom.as_view()), name="ChatRoom"),
      url('^logout/$','django.contrib.auth.views.logout',name='logout'),
      url('^Call/$', login_required(CallView.as_view()), name="Call"),
    url('^chatMessage/$', 'TaskManager.views.chatMessage', name="chatMessage"),
    url('^SendMail/$', 'TaskManager.views.SendMail', name="SendMail"),
    url('^ChangeTheme/$', 'TaskManager.views.ChangeTheme', name="ChangeTheme"),
    url('^getTaskStatus/$', 'TaskManager.views.getTaskStatus', name="getTaskStatus"),
    url('^CreateMeetingRequest/$', 'TaskManager.views.CreateMeetingRequest', name="CreateMeetingRequest"),
    url('^getRSSFeed/$', 'TaskManager.views.getRSSFeed', name="getRSSFeed"),
    url('^setSessionMap/$', 'TaskManager.views.setSessionMap', name="setSessionMap"),

    url('^TaskTypeView/$', login_required(TaskTypeView.as_view()), name="TaskTypeView"),


)