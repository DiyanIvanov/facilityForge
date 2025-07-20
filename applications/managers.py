from django.db import models
from django.db.models import Q


class ApplicationModelManager(models.Manager):
    def pending_applications(self, user):
        query = Q(status='pending') & (Q(applicant=user.pk) | Q(team__team_owner=user.pk) | Q(facility__owner=user.pk))
        return self.filter(query)

