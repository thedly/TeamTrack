# Create your views here.
from django.views.generic.base import TemplateView
from BugTracker.forms import BugForm
from BugTracker.models import Bug

class BugView(TemplateView):
    template_name = "bugs.html"

    def get_context_data(self, **kwargs):
        context = super(BugView, self).get_context_data(**kwargs)
        context['LoginForm'] = BugForm()
        context['Bugs'] = Bug.objects.all()
        return context