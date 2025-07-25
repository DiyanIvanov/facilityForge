from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, FormView, DetailView
from tickets.models import Tickets, TicketMessages
from tickets.forms import CreateTicketForm, UpdateTicketForm, TicketMessageForm


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


class UpdateTicketView(LoginRequiredMixin, UpdateView):
    model = Tickets
    form_class = UpdateTicketForm
    template_name = 'tickets/update-ticket.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_messages'] = TicketMessages.objects.filter(ticket_id=self.object.id).order_by('created_at')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CreateTicketMessageView(LoginRequiredMixin, CreateView):
    model = TicketMessages
    form_class = TicketMessageForm
    template_name = 'tickets/update-ticket.html'

    def get_success_url(self):
        return reverse_lazy('update-ticket', kwargs={'pk': self.kwargs['pk']})

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.ticket_id = self.kwargs['pk']
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


@method_decorator(never_cache, name='dispatch')
class GetTicketsByFacilityOrPriorityView(LoginRequiredMixin, DetailView):
    model = Tickets
    http_method_names = ['get',]

    def get(self, request, *args, **kwargs):
        facility_id = request.GET.get('facility')
        priority = request.GET.get('priority')

        tickets = Tickets.objects.get_all_user_tickets(user=request.user)

        if facility_id:
            tickets = tickets.filter(facility_id=facility_id)

        if priority:
            tickets = tickets.filter(priority=priority)

        result = []
        for ticket in tickets:
            result.append({
                "ticket_id": ticket.id,
                "facility_name": ticket.facility.name if ticket.facility else None,
                "priority": ticket.priority,
                "status": ticket.status,
                "description": ticket.description,

            })

        return JsonResponse(result, safe=False)


