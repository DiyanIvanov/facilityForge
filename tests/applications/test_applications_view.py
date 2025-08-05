from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import Team
from applications.models import Applications
from facilities.models import Facility
from django.urls import reverse

UserModel = get_user_model()


class TeamApplicationViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='user', password='pass', email='user@test.com')
        self.other_user = UserModel.objects.create_user(username='other_user', password='pass', email='other_user@user.com')
        self.client.login(username='user', password='pass')

        self.team = Team.objects.create(name='Team A', team_owner=self.user, manager=self.user)
        self.team_two = Team.objects.create(name='Team B', team_owner=self.other_user, manager=self.other_user)
        self.facility = Facility.objects.create(name='Facility A', owner=self.user)

        self.app = Applications.objects.create(
            applicant=self.user,
            team=self.team,
            facility=self.facility,
            status='pending',
            description='Test app'
        )

    def test__create_team_application(self):
        response = self.client.post(f'/applications/{self.team_two.pk}/team-application/', {
            'description': 'New application'
        })
        self.assertIn(response.status_code, (301, 302))
        self.assertTrue(Applications.objects.filter(description='New application').exists())

    def test_create_team_application__with_invalid_team(self):
        response = self.client.post('/applications/999/team-application/', {
            'description': 'Invalid application'
        })
        self.assertEqual(response.status_code, 404)

    def test__double_team_application(self):
        response = self.client.post(f'/applications/{self.team_two.pk}/team-application/', {
            'description': 'New application'
        })
        self.assertIn(response.status_code, (301, 302))
        self.assertTrue(Applications.objects.filter(description='New application').exists())

        response = self.client.post(f'/applications/{self.team_two.pk}/team-application/', {
            'description': 'New application'
        })
        self.assertEqual(response.status_code, 403)

