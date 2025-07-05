from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView



UserModel = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    model = UserModel
    form_class = UserCreationForm
    template_name = 'accounts/register-page.html'
    # Todo: Change to Index when common app is created
    success_url = reverse_lazy('login')
