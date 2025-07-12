from django.urls import path

from facilities.views import FacilityManagement

urlpatterns = [
    path('', FacilityManagement.as_view(), name='facilityManagement'),
]
