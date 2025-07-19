from django.urls import path

from applications.views import ApplicationView, AcceptOrRejectApplicationView, SearchFacilitiesAndTeamsView

urlpatterns = [
    path('', ApplicationView.as_view(), name='applications'),
    path('accept-reject/', AcceptOrRejectApplicationView.as_view(), name='accept_or_reject_application'),
    path('search/', SearchFacilitiesAndTeamsView.as_view(), name='search_facilities_and_teams'),
]