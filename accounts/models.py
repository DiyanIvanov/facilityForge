from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class FacilityForgeUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    # team = models.ManyToManyField(
    #     'Team',
    #     related_name='members',
    #     blank=True,
    # )
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

    def __str__(self):
        return self.username

