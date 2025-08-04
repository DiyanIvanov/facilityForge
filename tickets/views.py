from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DetailView
from tickets.models import Tickets, TicketMessages
from tickets.forms import CreateTicketForm, UpdateTicketForm, TicketMessageForm
from tickets.tasks import send_ticket_notification


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
        response = super().form_valid(form)

        send_ticket_notification.delay(
            ticket_id=form.instance.id,
            username=self.request.user.username,
            user_email=self.request.user.email,
            ticket_title=form.instance.title
        )
        return response


class UpdateTicketView(LoginRequiredMixin, UpdateView):
    model = Tickets
    form_class = UpdateTicketForm
    template_name = 'tickets/update-ticket.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset =None):
        ticket = super().get_object(queryset)

        created_by_user = ticket.created_from == self.request.user
        user_is_facility_owner = ticket.facility.owner == self.request.user
        is_users_team_assigned = False
        if ticket.assigned_to:
            is_users_team_assigned = ticket.assigned_to.members.filter(id=self.request.user.id).exists()

        if not (created_by_user or user_is_facility_owner or is_users_team_assigned):
            raise PermissionDenied("You do not have permission to update this ticket.")

        if ticket.status == 'closed':
            raise PermissionDenied("You cannot update a closed ticket.")

        return ticket

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

    def get_object(self, queryset =None):
        ticket = Tickets.objects.get(id=self.kwargs['pk'])

        created_by_user = ticket.created_from == self.request.user
        user_is_facility_owner = ticket.facility.owner == self.request.user
        is_users_team_assigned = False
        if ticket.assigned_to:
            is_users_team_assigned = ticket.assigned_to.members.filter(id=self.request.user.id).exists()

        if not (created_by_user or user_is_facility_owner or is_users_team_assigned):
            raise PermissionDenied("You do not have permission to add a message to this ticket.")

        return super().get_object(queryset)

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
