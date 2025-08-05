from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, TemplateView, CreateView
from django.apps import apps

from accounts.models import Team
from applications.forms import ApplicationForm, TeamApplicationForm, FacilityApplicationForm
from applications.models import Applications


# Create your views here.
class ApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'applications/applications.html'
    model = Applications
    context_object_name = 'applications'

    def get_queryset(self):
        return Applications.objects.pending_applications(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['teams'] = apps.get_model('accounts', 'Team').objects.teams_user_is_not_involved_in(self.request.user)
        context['facilities'] = apps.get_model('facilities', 'Facility').objects.facilities_user_is_not_involved_in(self.request.user)
        return context


class AcceptOrRejectApplicationView(LoginRequiredMixin, FormView):
    form_class = ApplicationForm
    template_name = 'applications/applications.html'

    def form_valid(self, form):
        application_id = form.cleaned_data['id']
        action = form.cleaned_data['action']
        try:
            application = Applications.objects.get(pk=application_id)
            # todo: check if the user is allowed to accept or reject this application
            # For now, we assume the user is allowed to accept or reject any application
            if action == 'accept':
                self.accept_application(application)
            elif action == 'reject':
                application.status = 'rejected'
            elif action == 'cancel':
                application.status = 'Cancelled'

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

    def accept_application(self, application):
        application.status = 'approved'
        if application.team and application.facility:
            # If both team and facility are present, we assume the application is for a team to use a facility
            application.facility.engineering_teams.add(application.team)
            application.facility.save()
        elif application.team:
            # If only team is present, we assume the application is for a team
            application.team.members.add(application.applicant)
            application.team.save()
        elif application.facility:
            # If only facility is present, we assume the application is for a facility
            application.facility.tenants.add(application.applicant)
            application.facility.save()
        application.save()
        return 0

class SearchFacilitiesAndTeamsView(LoginRequiredMixin, View):
    teams_model = apps.get_model('accounts', 'Team')
    facility_model = apps.get_model('facilities', 'Facility')


    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        results = []

        teams = self.teams_model.objects.teams_user_is_not_involved_in(request.user)
        facilities = self.facility_model.objects.facilities_user_is_not_involved_in(request.user)

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


class  TeamApplicationView(LoginRequiredMixin, CreateView):
    template_name = 'applications/team-application.html'
    form_class = TeamApplicationForm
    success_url = reverse_lazy('applications')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = apps.get_model(app_label='accounts', model_name='Team').objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        try:
            team = apps.get_model(app_label='accounts', model_name='Team').objects.get(pk=self.kwargs['pk'])
        except Team.DoesNotExist:
            raise Http404

        # check if user is allowed to apply to this team
        if not Team.objects.is_user_allowed_to_apply(self.request.user, team):
            raise PermissionDenied

        form.instance.applicant = self.request.user
        form.instance.team = team
        form.instance.status = 'pending'
        form.save()
        return super().form_valid(form)


class FacilityApplicationView(LoginRequiredMixin, CreateView):
    template_name = 'applications/facility-application.html'
    form_class = FacilityApplicationForm
    success_url = reverse_lazy('applications')
    facility_model = apps.get_model(app_label='facilities', model_name='Facility')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facility'] = self.facility_model.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            facility = self.facility_model.objects.get(pk=self.kwargs['pk'])
        except self.facility_model.DoesNotExist:
            raise Http404

        # check if user is allowed to apply to this facility
        if not self.facility_model.objects.is_user_allowed_to_apply(self.request.user, facility):
            raise PermissionDenied

        form.instance.applicant = self.request.user
        form.instance.facility = facility
        form.instance.status = 'pending'
        form.save()
        return super().form_valid(form)
