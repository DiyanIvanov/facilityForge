from django.contrib.auth.views import LoginView



class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    redirect_authenticated_user = True

