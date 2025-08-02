from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView, ListView, UpdateView
from accounts.forms import CustomRegisterForm, EditProfileForm, CreateTeamForm, RemoveMemberForm, EditTeamForm, \
    RemoveFacilityForm
from accounts.models import Team
from django.contrib.auth import login

from facilityForge.mixins import DeleteObjectMixin

UserModel = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    model = UserModel
    form_class = CustomRegisterForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


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
        context['teams'] = Team.objects.all_user_teams(self.request.user)
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

@method_decorator(never_cache, name='dispatch')
class EditTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = EditTeamForm
    template_name = 'teams/edit-team.html'
    success_url = reverse_lazy('teams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['team_owner'] = obj.team_owner
        context['team_members'] = obj.members.all()
        context['facilities'] = obj.serviced_facilities.all()

        return context

    def get_object(self, queryset=None):
        team = super().get_object(queryset)

        if team.team_owner != self.request.user and not team.members.filter(id=self.request.user.id).exists():
            raise PermissionError("You are not a member of this team.")

        return team

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        if self.request.user != self.get_object().team_owner:
            raise PermissionError("Only the team owner can make changes.")

        form.save()
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class RemoveMemberView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = RemoveMemberForm
    http_method_names = ['post']

    def get_object(self, queryset=None):
        team = super().get_object()

        if team.team_owner != self.request.user and not team.members.filter(id=self.request.user.id).exists():
            raise PermissionError("You are not a member of this team.")

        return team

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        member_id = form.cleaned_data['member_id']
        member = form.instance.members.get(id=member_id)
        team_obj = self.get_object()

        is_owner = self.request.user == team_obj.team_owner
        is_member = self.request.user == member
        if not is_member and not is_owner:
            raise PermissionError("You cannot remove this member from the team.")

        if member:
            team_obj.members.remove(member)
            team_obj.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(never_cache, name='dispatch')
class RemoveFacilityView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = RemoveFacilityForm
    http_method_names = ['post']

    def get_object(self, queryset=None):
        team = super().get_object()
        facility_id = self.request.POST.get('facility_id')
        facility = team.serviced_facilities.filter(id=facility_id).first()

        if not facility:
            raise ValueError("This facility is not serviced by this team.")

        if team.team_owner != self.request.user \
            and not team.members.filter(id=self.request.user.id).exists() \
            and facility.owner != self.request.user:
                raise PermissionError("You are neither member of this team or facility owner.")

        return team

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        facility_id = form.cleaned_data['facility_id']
        facility = form.instance.serviced_facilities.get(id=facility_id)

        if facility:
            team_obj = self.get_object()
            team_obj.serviced_facilities.remove(facility)
            team_obj.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(never_cache, name='dispatch')
class DeleteTeamView(LoginRequiredMixin, DeleteObjectMixin):
    model = Team
    template_name = 'teams/delete-team.html'
    success_url = reverse_lazy('teams')
    message = 'This team cannot be deleted at this time.'
    fail_url = 'edit-team'

    def get_object(self, queryset=None):
        team = super().get_object(queryset)

        if team.team_owner != self.request.user:
            raise PermissionError("Only team owner can delete the team.")

        return team
