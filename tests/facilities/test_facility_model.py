from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from facilities.models import Facility

UserModel = get_user_model()

class FacilityModelTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username='owner', email='owner@example.com', password='pass'
        )

    def test__facility_str_method__returns_name(self):
        facility = Facility.objects.create(name="Test Facility", owner=self.owner)
        self.assertEqual(str(facility), "Test Facility")

    def test__facility_name_unique_constraint__raises_integrity_error(self):
        Facility.objects.create(name="Unique Facility", owner=self.owner)
        with self.assertRaises(IntegrityError):
            Facility.objects.create(name="Unique Facility", owner=self.owner)

    def test__facility_created_with_required_fields__successfully_saved(self):
        facility = Facility.objects.create(name="Required Only", owner=self.owner)
        self.assertTrue(Facility.objects.filter(name="Required Only").exists())

    def test__facility_optional_fields__accept_blank_or_null(self):
        facility = Facility.objects.create(
            name="Optional Fields",
            owner=self.owner,
            description='',
            location=None,
            postcode=None,
            manager=None
        )
        self.assertIsNone(facility.manager)
        self.assertEqual(facility.description, '')

    def test__facility_ordering__orders_by_name(self):
        Facility.objects.create(name="B Facility", owner=self.owner)
        Facility.objects.create(name="A Facility", owner=self.owner)
        names = list(Facility.objects.values_list('name', flat=True))
        self.assertEqual(names, sorted(names))
