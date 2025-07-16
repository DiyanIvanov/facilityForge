from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from applications.models import Applications


# Create your views here.
class ApplicationView(LoginRequiredMixin, ListView):
    template_name = 'applications/applications.html'
    model = Applications
    context_object_name = 'applications'

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user).order_by('-id')
