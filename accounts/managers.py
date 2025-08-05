from django.db.models import Manager, Q


class TeamManager(Manager):
    def teams_user_is_not_involved_in(self, user):
        query = Q(team_owner=user) | Q(members=user) | Q(manager=user) \
                | Q(applications__status='accepted') | Q(applications__status='pending')
        return self.exclude(query).distinct()

    def all_user_teams(self, user):
        query = Q(team_owner=user) | Q(members=user) | Q(manager=user)
        return self.filter(query).distinct()

    def is_user_allowed_to_apply(self, user, team):
        team = self.get(pk=team.pk)
        if team.team_owner == user or team.manager == user:
            return False
        if team.applications.filter(applicant=user, status__in=['pending']).exists():
            return False
        if team.members.filter(pk=user.pk).exists():
            return False
        return True