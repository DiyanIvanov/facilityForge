from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import TeamManager


# Create your models here.
class FacilityForgeUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # facilities = models.ManyToManyField(
    #     'facilities.Facility',
    #     related_name='users',
    #     blank=True,
    # )
    # tickets = models.ManyToManyField(
    #     'tickets.Ticket',
    #     related_name='users',
    #     blank=True,
    # )
    # applications = models.ManyToManyField(
    #     'applications.Application',
    #     related_name='users',
    #     blank=True
    # )

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    moto = models.CharField(max_length=200, blank=True, null=True)
    team_owner = models.ForeignKey(
        FacilityForgeUser,
        on_delete=models.CASCADE,
        related_name='owned_teams',
    )
    manager = models.ForeignKey(
        FacilityForgeUser,
        on_delete=models.CASCADE,
        related_name='managed_teams',
    )
    members = models.ManyToManyField(
        FacilityForgeUser,
        related_name='teams',
        blank=True,
    )
    # tickets = models.ManyToManyField(
    #     'tickets.Ticket',
    #     related_name='teams',
    #     blank=True,
    #     null=True
    # )

    objects = TeamManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Teams'