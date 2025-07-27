from django.db import models
from applications.managers import ApplicationModelManager

class Applications(models.Model):
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('cancel', 'Cancelled')
        ],
        default='pending'
    )
    applicant = models.ForeignKey(
        'accounts.FacilityForgeUser',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    team = models.ForeignKey(
        'accounts.Team',
        on_delete=models.CASCADE,
        related_name='applications',
        blank=True,
        null=True
    )
    facility = models.ForeignKey(
        'facilities.Facility',
        on_delete=models.CASCADE,
        related_name='applications',
        blank=True,
        null=True
    )

    objects = ApplicationModelManager()

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-created']
