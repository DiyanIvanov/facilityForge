from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
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

@method_decorator(never_cache, name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'


