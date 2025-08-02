from django.urls import path, include

from facilities.views import FacilityManagement, CreateFacility, EditFacilityView, RemoveTenantView, DeleteFacilityView

urlpatterns = [
    path('', FacilityManagement.as_view(), name='facilities'),
    path('create/', CreateFacility.as_view(), name='create-facility'),
    path('<int:pk>/', include([
        path('edit-facility/', EditFacilityView.as_view(), name='edit-facility'),
        path('remove-tenant/', RemoveTenantView.as_view(), name='remove-tenant'),
        path('delete/', DeleteFacilityView.as_view(), name='delete-facility'),
    ]))
]
