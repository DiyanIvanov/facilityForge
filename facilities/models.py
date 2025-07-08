from django.db import models


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
    owner = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE
    )
    manager = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        'accounts.FacilityForgeUser',
        related_name='facilities',
        blank=True
    )
    engineering_team = models.ForeignKey(
        'accounts.Team',
        on_delete=models.CASCADE,
        related_name='engineering_facilities',
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ['name']

