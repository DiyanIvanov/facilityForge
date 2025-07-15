from django.contrib.auth.views import LogoutView
from django.urls import path, include
from accounts.views import CustomLoginView, RegisterView, EditProfileView, CreateTeam, TeamsView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', include([
        path('', EditProfileView.as_view(), name='edit-profile'),

    ])),
    path('teams/', include([
    path('', TeamsView.as_view(), name='teams'),
        path('create/', CreateTeam.as_view(), name='create-team'),
    ])),
]