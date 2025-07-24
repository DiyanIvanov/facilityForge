from django.urls import path, include

from tickets.views import CreateTicketView, UpdateTicketView

urlpatterns = [
    path('create-ticket/', CreateTicketView.as_view(), name='create-ticket'),
    path('<int:pk>/', include([
        path('update/', UpdateTicketView.as_view(), name='update-ticket'),

    ]))
]