from django.db import models

# Create your models here.

class Applications(models.Model):
    application_id = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
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

    def __str__(self):
        return self.application_id

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'