from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView

from applications.forms import ApplicationForm
from applications.models import Applications


# Create your views here.
class ApplicationView(LoginRequiredMixin, ListView):
    template_name = 'applications/applications.html'
    model = Applications
    context_object_name = 'applications'

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user).order_by('-id')



class AcceptOrRejectApplicationView(LoginRequiredMixin, FormView):
    form_class = ApplicationForm
    template_name = 'applications/applications.html'

    def form_valid(self, form):
        application_id = form.cleaned_data['application_id']
        action = form.cleaned_data['action']
        try:
            application = Applications.objects.get(application_id=application_id)

            if action == 'accept':
                application.status = 'approved'
            elif action == 'reject':
                application.status = 'rejected'

            application.save()
            return JsonResponse({
                'success': True,
                'status': application.status,
                'id': application_id
            })

        except Applications.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Application not found',
                'id': application_id
            }, status=404)

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'error': 'Invalid form submission',
            'form_errors': form.errors
        }, status=400)
