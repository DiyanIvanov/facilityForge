from django.urls import path, include

from tickets.views import CreateTicketView

urlpatterns = [
    path('create-ticket/', CreateTicketView.as_view(), name='create-ticket'),
]