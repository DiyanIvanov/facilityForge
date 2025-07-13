from django.urls import path

from facilities.views import FacilityManagement, CreateFacility

urlpatterns = [
    path('', FacilityManagement.as_view(), name='facilities'),
    path('create/', CreateFacility.as_view(), name='create-facility'),
    # path('<int:pk>/', FacilityDetails.as_view(), name='facility-detail'),

]
