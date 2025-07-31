from django.urls import path

from facilities.views import FacilityManagement, CreateFacility, EditFacilityView

urlpatterns = [
    path('', FacilityManagement.as_view(), name='facilities'),
    path('create/', CreateFacility.as_view(), name='create-facility'),
    path('<int:pk>/edit-facility/', EditFacilityView.as_view(), name='edit-facility'),

]
