from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, FormView, TemplateView
from django.apps import apps
from applications.forms import ApplicationForm
from applications.models import Applications


# Create your views here.
class ApplicationView(LoginRequiredMixin, ListView):
    template_name = 'applications/applications.html'
    model = Applications
    context_object_name = 'applications'

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['teams'] = apps.get_model('accounts', 'Team').objects.all()
        context['facilities'] = apps.get_model('facilities', 'Facility').objects.all()
        return context


class AcceptOrRejectApplicationView(LoginRequiredMixin, FormView):
    form_class = ApplicationForm
    template_name = 'applications/applications.html'

    def form_valid(self, form):
        application_id = form.cleaned_data['application_id']
        action = form.cleaned_data['action']
        try:
            application = Applications.objects.get(application_id=application_id)
            # todo: check if the user is allowed to accept or reject this application
            # For now, we assume the user is allowed to accept or reject any application
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


class SearchFacilitiesAndTeamsView(LoginRequiredMixin, View):
    teams_model = apps.get_model('accounts', 'Team')
    facility_model = apps.get_model('facilities', 'Facility')


    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        results = []

        teams = self.teams_model.objects.all()
        facilities = self.facility_model.objects.all()

        if query:
            teams = self.teams_model.objects.filter(name__icontains=query)
            facilities = self.facility_model.objects.filter(name__icontains=query)

        for team in teams:
            results.append({
                'type': 'team',
                'pk': team.pk,
                'name': team.name,
                'description': team.description,
                'moto': team.moto,
            })

        for facility in facilities:
            results.append({
                'type': 'facility',
                'pk': facility.pk,
                'name': facility.name,
                'description': facility.description,
            })

        return JsonResponse({'results': results}, safe=False)
