from django.db.models import Manager, Q


class TeamManager(Manager):
    def teams_user_is_not_involved_in(self, user):
        query = Q(team_owner=user) | Q(members=user) | Q(manager=user) \
                | Q(applications__status='accepted') | Q(applications__status='pending')
        return self.exclude(query).distinct()

    def all_user_teams(self, user):
        query = Q(team_owner=user) | Q(members=user) | Q(manager=user)
        return self.filter(query).distinct()