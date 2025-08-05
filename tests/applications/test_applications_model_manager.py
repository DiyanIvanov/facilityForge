from django.test import TestCase
from django.contrib.auth import get_user_model
from applications.models import Applications
from accounts.models import Team
from facilities.models import Facility

User = get_user_model()

class ApplicationModelManagerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='main@test.com', password='pass')
        self.other_user = User.objects.create_user(username='other', email='other@test.com', password='pass')

        self.team = Team.objects.create(name='Team 1', team_owner=self.user, manager=self.user)
        self.facility = Facility.objects.create(name='Facility 1', owner=self.user)

    def test__user_is_applicant(self):
        app = Applications.objects.create(applicant=self.user, status='pending', description='Test A')
        result = Applications.objects.pending_applications(self.user)
        self.assertIn(app, result)

    def test__user_is_team_owner(self):
        app = Applications.objects.create(team=self.team, status='pending', description='Test B', applicant=self.other_user)
        result = Applications.objects.pending_applications(self.user)
        self.assertIn(app, result)

    def test__user_is_facility_owner(self):
        app = Applications.objects.create(facility=self.facility, status='pending', description='Test C', applicant=self.other_user)
        result = Applications.objects.pending_applications(self.user)
        self.assertIn(app, result)

    def test__non_pending_applications(self):
        Applications.objects.create(applicant=self.user, status='approved', description='Test D')
        Applications.objects.create(applicant=self.user, status='rejected', description='Test E')
        Applications.objects.create(applicant=self.user, status='cancel', description='Test F')
        result = Applications.objects.pending_applications(self.user)
        self.assertEqual(result.count(), 0)

    def test__unrelated_user__returns_empty_queryset(self):
        Applications.objects.create(status='pending', description='Test E', applicant=self.other_user)
        result = Applications.objects.pending_applications(self.user)
        self.assertEqual(result.count(), 0)