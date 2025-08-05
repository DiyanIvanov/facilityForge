from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import FacilityForgeUser, Team
from facilities.models import Facility
from applications.models import Applications


class ApplicationsModelTests(TestCase):
    def setUp(self):
        self.user = FacilityForgeUser.objects.create_user(
            username='applicant',
            email='user@test.com',
            password='pass'
        )

        self.team = Team.objects.create(
            name='Test Team',
            team_owner=self.user,
            manager=self.user
        )

        self.facility = Facility.objects.create(
            name='Test Facility',
            owner=self.user
        )

    def test__default_status_field__set_to_pending(self):
        app = Applications.objects.create(
            description='Request default',
            applicant=self.user
        )
        self.assertEqual(app.status, 'pending')

    def test__status_field__rejects_invalid_choice(self):
        app = Applications(
            description='Invalid',
            applicant=self.user,
            status='invalid_choice'
        )
        with self.assertRaises(ValidationError):
            app.full_clean()