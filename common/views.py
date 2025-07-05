from django.shortcuts import redirect
from django.views.generic import TemplateView


# Create your views here.
class IndexPageView(TemplateView):
    template_name = 'common/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)



class AboutPageView(TemplateView):
    template_name = 'common/about.html'
    #todo add tickets and facilities data when models are ready
    extra_context = {
        'tickets': None,
        'facilities': None,
    }

class DashboardView(TemplateView):
    template_name = 'common/dashboard.html'


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
