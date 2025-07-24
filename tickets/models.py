from django.db import models

from tickets.choices import TicketStatusChoices, TicketPriorityChoices
from tickets.managers import TicketManager


class Tickets(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=TicketStatusChoices.choices,
        default=TicketStatusChoices.OPEN
    )
    priority = models.CharField(
        max_length=50,
        choices=TicketPriorityChoices.choices,
        default=TicketPriorityChoices.LOW
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_from = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )
    facility = models.ForeignKey(
        'facilities.Facility',
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    assigned_to = models.ForeignKey(
        'accounts.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    objects = TicketManager()

    def __str__(self):
        return self.title


class TicketMessages(models.Model):

    class Meta:
        ordering = ['created_at']

    ticket = models.ForeignKey(
        Tickets,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} on {self.created_at}'
