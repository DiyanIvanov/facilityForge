from django.shortcuts import render
from django.views.generic import TemplateView


class FacilityManagement(TemplateView):
    template_name = 'account_management/facilities.html'
    extra_context = {
        'title': 'Facilities',
        'description': 'Manage your facilities efficiently with FacilityForge. Add, edit, and view details of your facilities.'
    }