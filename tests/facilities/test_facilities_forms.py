from django.test import TestCase
from django.contrib.auth import get_user_model
from facilities.models import Facility
from facilities.forms import UpdateFacilityForm, DeleteFacilityForm

UserModel = get_user_model()

class UpdateFacilityFormTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(username='owner', email='owner@example.com', password='pass')
        self.other_user = UserModel.objects.create_user(username='other', email='other@example.com', password='pass')

        self.facility = Facility.objects.create(
            name='Test Facility',
            location='Test Location',
            postcode='xx2 4yy',
            status='active',
            description='Test description',
            owner=self.owner
        )

    def test__status_field_is_disabled_for_all_users__field_disabled(self):
        form = UpdateFacilityForm(instance=self.facility, user=self.owner)
        self.assertTrue(form.fields['status'].disabled)

    def test__user_is_owner__only_status_disabled(self):
        form = UpdateFacilityForm(instance=self.facility, user=self.owner)
        disabled_fields = [name for name, field in form.fields.items() if field.disabled]
        self.assertIn('status', disabled_fields)
        self.assertNotIn('name', disabled_fields)
        self.assertNotIn('location', disabled_fields)
        self.assertNotIn('postcode', disabled_fields)
        self.assertNotIn('description', disabled_fields)

    def test__user_is_not_owner__all_fields_disabled(self):
        form = UpdateFacilityForm(instance=self.facility, user=self.other_user)
        for field in form.fields.values():
            self.assertTrue(field.disabled)


class DeleteFacilityFormTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='owner', email='owner@example.com', password='pass'
        )

        self.facility = Facility.objects.create(
            name='Test Facility',
            location='Test Location',
            postcode='12345',
            status='active',
            description='Test description',
            owner=self.user
        )

    def test__all_fields_readonly(self):
        form = DeleteFacilityForm(instance=self.facility)
        for name, field in form.fields.items():
            self.assertTrue(field.widget.attrs.get('readonly', False))
