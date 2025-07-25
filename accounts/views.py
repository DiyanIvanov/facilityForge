from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView, ListView, UpdateView

from accounts.forms import CustomRegisterForm, EditProfileForm, CreateTeamForm
from accounts.models import Team

UserModel = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    model = UserModel
    form_class = CustomRegisterForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')


@method_decorator(never_cache, name='dispatch')
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = EditProfileForm
    template_name = 'accounts/edit-user.html'
    success_url = reverse_lazy('edit-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class TeamsView(LoginRequiredMixin, ListView):
    template_name = 'teams/teams.html'
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = self.request.user.owned_teams.all()
        return context

class CreateTeam(LoginRequiredMixin, CreateView):
    template_name = 'teams/create-team.html'
    form_class = CreateTeamForm
    success_url = reverse_lazy('teams')

    def form_valid(self, form):
        form.instance.team_owner = self.request.user
        form.instance.manager = self.request.user
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('edit-profile')

