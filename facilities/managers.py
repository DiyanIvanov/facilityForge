from django.db.models import  Manager, Q


class FacilityManager(Manager):

    def facilities_user_is_not_involved_in(self, user):
        user_teams = user.owned_teams.all() | user.managed_teams.all()
        team_ids = user_teams.values_list('id', flat=True)

        direct_involvement = (
                Q(owner=user) |
                Q(manager=user) |
                Q(tenants=user) |
                Q(engineering_teams__in=team_ids)
        )

        return self.exclude(direct_involvement).distinct()

    def facilities_user_is_involved_in(self, user):
        user_teams = user.owned_teams.all() | user.managed_teams.all()
        team_ids = user_teams.values_list('id', flat=True)

        direct_involvement = (
            Q(owner=user) |
            Q(manager=user) |
            Q(tenants=user) |
            Q(engineering_teams__in=team_ids)
        )

        return self.filter(direct_involvement).distinct()

    def is_user_allowed_to_apply(self, user, facility):
        facility = self.get(pk=facility.pk)
        if facility.owner == user or facility.manager == user:
            return False
        if facility.applications.filter(applicant=user, status__in=['pending']).exists():
            return False
        if facility.tenants.filter(pk=user.pk).exists():
            return False
        if facility.engineering_teams.filter(Q(members=user) | Q(team_owner=user) | Q(manager=user)).exists():
            return False
        return True
