from django.db import models

from tickets.choices import TicketStatusChoices


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=TicketStatusChoices.choices,
        default=TicketStatusChoices.OPEN
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

    def __str__(self):
        return self.title
