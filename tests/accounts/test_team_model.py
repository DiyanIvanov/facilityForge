from django.db.models import QuerySet
from django.test import TestCase
from accounts.models import FacilityForgeUser
from accounts.models import Team
from tickets.models import Tickets  # Adjust import if needed

class TeamModelTest(TestCase):
    def setUp(self):
        self.owner = FacilityForgeUser.objects.create_user(
            username='owner', email='owner@test.com', password='TestPass'
        )
        self.manager = FacilityForgeUser.objects.create_user(
            username='manager', email='manager@test.com', password='TestPass'
        )
        self.member1 = FacilityForgeUser.objects.create_user(
            username='member1', email='member1@test.com', password='TestPass'
        )
        self.member2 = FacilityForgeUser.objects.create_user(
            username='member2', email='member2@test.com', password='TestPass'
        )
        self.member3 = FacilityForgeUser.objects.create_user(
            username='member3', email='member2@test.com', password='TestPass'
        )

        self.team = Team.objects.create(
            name='Test Team',
            description='A team for testing purposes',
            moto='Testing is fun!',
            team_owner=self.owner,
            manager=self.manager
        )

        self.team.members.add(self.member1, self.member2)

    def test__team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A team for testing purposes')
        self.assertEqual(self.team.moto, 'Testing is fun!')
        self.assertEqual(self.team.team_owner, self.owner)
        self.assertEqual(self.team.manager, self.manager)
        self.assertIn(self.member1, self.team.members.all())
        self.assertIn(self.member2, self.team.members.all())

    def test__all_user_teams__returns_correct_teams(self):
        teams = Team.objects.all_user_teams(self.member1)
        team_names = {t.name for t in teams}
        self.assertSetEqual(team_names, {'Test Team'})

    def test__all_user_teams__returns_empty_teams(self):
        teams = Team.objects.all_user_teams(self.member3)
        self.assertEqual(len(teams), 0)

    def test__teams_user_is_not_involved_in__returns_correct_teams(self):
        teams = Team.objects.teams_user_is_not_involved_in(self.member3)
        team_names = {t.name for t in teams}
        self.assertSetEqual(team_names, {'Test Team'})

    def test__teams_user_is_not_involved_in__does_not_return_user_teams(self):
        teams = Team.objects.teams_user_is_not_involved_in(self.member2)
        self.assertEqual(len(teams), 0)
