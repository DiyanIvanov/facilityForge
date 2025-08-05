from django.test import TestCase
from accounts.models import FacilityForgeUser, Team
from accounts.forms import EditTeamForm


class EditTeamFormTest(TestCase):
    def setUp(self):
        self.owner = FacilityForgeUser.objects.create_user(username='owner', email='owner@example.com', password='pass')
        self.manager = FacilityForgeUser.objects.create_user(username='manager', email='manager@example.com', password='pass')
        self.team = Team.objects.create(
            name='Team A',
            team_owner=self.owner,
            manager=self.manager,
            moto='Go Go Go',
            description='Original description'
        )

    def test__fields_enabled_for_team_owner(self):
        form = EditTeamForm(instance=self.team, user=self.owner)
        self.assertFalse(form.fields['name'].disabled)
        self.assertFalse(form.fields['moto'].disabled)
        self.assertFalse(form.fields['description'].disabled)

    def test__fields_disabled_for_non_owner(self):
        form = EditTeamForm(instance=self.team, user=self.manager)
        self.assertTrue(form.fields['name'].disabled)
        self.assertTrue(form.fields['moto'].disabled)
        self.assertTrue(form.fields['description'].disabled)

    def test__fields_disabled_if_user_not_provided(self):
        form = EditTeamForm(instance=self.team)
        self.assertTrue(form.fields['name'].disabled)
        self.assertTrue(form.fields['moto'].disabled)
        self.assertTrue(form.fields['description'].disabled)