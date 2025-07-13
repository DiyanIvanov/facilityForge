from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from accounts.forms import CustomRegisterForm, EditProfileForm

UserModel = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    model = UserModel
    form_class = CustomRegisterForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')


class EditProfileView(FormView):
    model = UserModel
    form_class = EditProfileForm
    template_name = 'accounts/edit-user.html'
    success_url = reverse_lazy('dashboard')


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
