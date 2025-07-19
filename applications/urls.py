from django.urls import path, include

from applications.views import ApplicationsView, AcceptOrRejectApplicationView, SearchFacilitiesAndTeamsView, \
    TeamApplicationView

urlpatterns = [
    path('', ApplicationsView.as_view(), name='applications'),
    path('accept-reject/', AcceptOrRejectApplicationView.as_view(), name='accept_or_reject_application'),
    path('search/', SearchFacilitiesAndTeamsView.as_view(), name='search_facilities_and_teams'),
    path('<int:pk>/', include([
        path('team-application/', TeamApplicationView.as_view(), name='team_application'),
    ])),
]