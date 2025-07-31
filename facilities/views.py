from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, ListView, UpdateView
from facilities.models import Facility
from facilities.forms import CreateFacilityForm, UpdateFacilityForm, RemoveTenantForm


class FacilityManagement(LoginRequiredMixin, ListView):
    model = Facility
    template_name = 'facilities/facilities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = self.model.objects.facilities_user_is_involved_in(self.request.user)
        return context


class CreateFacility(LoginRequiredMixin, CreateView):
    template_name = 'facilities/create-facility.html'
    form_class = CreateFacilityForm
    success_url = reverse_lazy('facilities')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.manager = self.request.user
        return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
class EditFacilityView(LoginRequiredMixin, UpdateView):
    model = Facility
    form_class = UpdateFacilityForm
    template_name = 'facilities/edit-facility.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        facility = super().get_object(queryset)

        user_ids_from_service_teams = Facility.objects.facilities_user_is_involved_in(self.request.user).values_list('id', flat=True)

        if facility.owner != self.request.user \
                and self.request.user not in facility.tenants.all() \
                and self.request.user.id not in user_ids_from_service_teams:
            raise PermissionDenied("You do not have permission to edit this facility.")

        return facility

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facility_object = self.get_object()
        context['tenants'] = facility_object.tenants.all()
        context['service_teams'] = facility_object.engineering_teams.all()
        context['owner'] = facility_object.owner
        return context

    def form_valid(self, form):
        if form.instance.owner != self.request.user and self.request.user not in form.instance.tenants.all():
            raise PermissionDenied("You do not have permission to edit this facility.")
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class RemoveTenantView(LoginRequiredMixin, UpdateView):
    model = Facility
    form_class = RemoveTenantForm
    http_method_names = ['post']
    facility = None

    def get_success_url(self):

        if self.request.user == self.facility.owner:
            return self.request.META.get('HTTP_REFERER')

        return reverse_lazy('facilities')

    def get_object(self, queryset=None):
        facility = super().get_object(queryset)

        if facility.owner != self.request.user and self.request.user not in facility.tenants.all():
            raise PermissionDenied("You do not have permission to remove tenants from this facility.")

        return facility

    def form_valid(self, form):
        tenant_id = form.cleaned_data['tenant_id']
        tenant = form.instance.tenants.filter(id=tenant_id)

        if not tenant:
            raise PermissionDenied("Tenant does not exist or you do not have permission to remove them.")

        self.facility = self.get_object()
        self.facility.tenants.remove(tenant.first())
        self.facility.save()

        return super().form_valid(form)
