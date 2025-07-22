from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.apps import apps


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


@method_decorator(never_cache, name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = apps.get_model(
            'tickets',
            'Tickets'
        ).objects.get_all_user_tickets(user=self.request.user)
        # todo: add all facilities user is involved wit, when custom manager is implemented
        context['facilities'] = self.request.user.owned_facilities.all()
        return context
