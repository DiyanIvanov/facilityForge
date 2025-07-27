from django.db import models

from facilities.managers import FacilityManager


class Facility(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    postcode = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        default='active'
    )
    owner = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE,
        related_name='owned_facilities',
    )
    manager = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE,
        related_name='managed_facilities',
        blank=True,
        null=True
    )
    tenants = models.ManyToManyField(
        'accounts.FacilityForgeUser',
        related_name='used_facilities',
        blank=True,
    )
    engineering_teams = models.ManyToManyField(
        'accounts.Team',
        related_name='serviced_facilities',
        blank=True,
    )


    objects = FacilityManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ['name']

