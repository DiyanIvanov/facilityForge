from django.urls import path, include
from tickets.views import CreateTicketMessageView
from tickets.views import CreateTicketView, UpdateTicketView

urlpatterns = [
    path('create-ticket/', CreateTicketView.as_view(), name='create-ticket'),
    path('<int:pk>/', include([
        path('update/', UpdateTicketView.as_view(), name='update-ticket'),
        path('ticket-message/', CreateTicketMessageView.as_view(), name='create-ticket-message'),
    ])),

]