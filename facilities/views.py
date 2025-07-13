from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from facilities.models import Facility
from facilities.forms import CreateFacilityForm


class FacilityManagement(LoginRequiredMixin, ListView):
    template_name = 'facilities/facilities.html'
    model = Facility

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = self.request.user.owned_facilities.all()
        return context


class CreateFacility(LoginRequiredMixin, CreateView):
    template_name = 'facilities/create-facility.html'
    form_class = CreateFacilityForm
    success_url = reverse_lazy('facilities')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.manager = self.request.user
        return super().form_valid(form)
