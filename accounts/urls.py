from django.contrib.auth.views import LogoutView
from django.urls import path, include
from accounts.views import CustomLoginView, RegisterView, EditProfileView, CreateTeam, TeamsView, ChangePasswordView, \
    EditTeamView, RemoveMemberView, RemoveFacilityView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', include([
        path('', EditProfileView.as_view(), name='edit-profile'),

    ])),
    path('teams/', include([
        path('', TeamsView.as_view(), name='teams'),
        path('create/', CreateTeam.as_view(), name='create-team'),
        path('<int:pk>/', include([
            path('remove-member/', RemoveMemberView.as_view(), name='remove-team-member'),
            path('remove-facility/', RemoveFacilityView.as_view(), name='remove-facility'),
            path('edit/', EditTeamView.as_view(), name='edit-team'),
        ]))
    ])),

]