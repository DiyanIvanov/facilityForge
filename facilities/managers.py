from django.db.models import  Manager, Q


class FacilityManager(Manager):
    def facilities_user_is_not_involved_in(self, user):
        query = Q(owner=user) | Q(manager=user) | Q(tenants=user) | Q(engineering_teams__members=user) \
                | Q(engineering_teams__team_owner=user) | Q(engineering_teams__manager=user) \
                | Q(engineering_teams__applications__status='accepted') | Q(engineering_teams__applications__status='pending') \
                | Q(applications__status='accepted') | Q(applications__status='pending')

        return self.exclude(query).distinct()