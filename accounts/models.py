from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.managers import TeamManager


# Create your models here.
class FacilityForgeUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    rating = models.PositiveSmallIntegerField(
        default=10,
        validators=[
            models.MinValueValidator(1),
            models.MaxValueValidator(10)
        ]
    )


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
    tickets = models.ManyToManyField(
        'tickets.Tickets',
        related_name='teams',
        blank=True,
    )

    objects = TeamManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Teams'