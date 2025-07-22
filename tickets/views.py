from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from tickets.models import Tickets
from tickets.forms import CreateTicketForm

class CreateTicketView(LoginRequiredMixin, CreateView):
    model = Tickets
    form_class = CreateTicketForm
    template_name = 'tickets/create-ticket.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_from = self.request.user
        return super().form_valid(form)
