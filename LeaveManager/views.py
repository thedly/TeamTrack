# Create your views here.
from django.views.generic.base import TemplateView
from django.core.mail import send_mass_mail, send_mail
from LeaveManager.models import LeavemanagerLeaves
from django.http import HttpResponse
from TaskManager.models import ExtendedUser
import logging
import datetime
import redis
from django.utils.html import strip_tags
log = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'LeaveManagerHome.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['Leaves'] = LeavemanagerLeaves.objects.filter(UserId=self.request.user.id)
        return context

def SendLeaveRequest(request):

    StartDate = datetime.datetime.fromtimestamp(int(request.GET['StartDate'])/1000)
    EndDate = datetime.datetime.fromtimestamp(int(request.GET['EndDate'])/1000)
    Purpose = request.GET['Purpose']
    UserId = request.user.id
    message = strip_tags(request.GET['Message'])
    LeavemanagerLeavesObj = LeavemanagerLeaves(StartDate=StartDate, EndDate=EndDate, UserId=ExtendedUser.objects.get(pk=UserId), Purpose=Purpose, emergencyleave=False, approved=False )

    LeavemanagerLeavesObj.save()
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.publish('chat', "Redis notification : Leave was created")
    #send_mail('Subject here', message, 'tejashedly@achumen.com', ['tj.werewolf@gmail.com', 'tejas.240489@gmail.com'], fail_silently=False)
    return HttpResponse("successfully sent mail")




