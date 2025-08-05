from django.test import TestCase
from accounts.models import FacilityForgeUser, Team
from applications.forms import FacilityApplicationForm

class FacilityApplicationFormTests(TestCase):
    def setUp(self):
        self.user = FacilityForgeUser.objects.create_user(
            username='user1', email='user1@test.com', password='pass'
        )
        self.other_user = FacilityForgeUser.objects.create_user(
            username='user2', email='user2@test.com', password='pass'
        )

        self.owned_team = Team.objects.create(name='Owned Team', team_owner=self.user, manager=self.other_user)
        self.managed_team = Team.objects.create(name='Managed Team', team_owner=self.other_user, manager=self.user)

        self.unrelated_team = Team.objects.create(name='Other Team', team_owner=self.other_user, manager=self.other_user)

    def test__team_queryset__includes_teams_owned_by_user(self):
        form = FacilityApplicationForm(user=self.user)
        self.assertIn(self.owned_team, form.fields['team'].queryset)

    def test__team_queryset__includes_teams_managed_by_user(self):
        form = FacilityApplicationForm(user=self.user)
        self.assertIn(self.managed_team, form.fields['team'].queryset)

    def test__team_queryset__excludes_unrelated_teams(self):
        form = FacilityApplicationForm(user=self.user)
        self.assertNotIn(self.unrelated_team, form.fields['team'].queryset)
