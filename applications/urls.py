from django.urls import path

from applications.views import ApplicationView, AcceptOrRejectApplicationView

urlpatterns = [
    path('', ApplicationView.as_view(), name='applications'),
    path('accept-reject/', AcceptOrRejectApplicationView.as_view(), name='accept_or_reject_application'),
]