from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from facilities.forms import CreateFacilityForm


class FacilityManagement(TemplateView):
    template_name = 'facilities/facilities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = self.request.user.owned_facilities.all()
        return context


class CreateFacility(CreateView):
    template_name = 'facilities/create-facility.html'
    form_class = CreateFacilityForm
    success_url = reverse_lazy('facilities')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.manager = self.request.user
        return super().form_valid(form)
