from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from facilities.models import Facility
from tickets.models import Tickets

UserModel = get_user_model()

class DeleteFacilityViewTests(TestCase):
    def setUp(self):
        # Users
        self.owner = UserModel.objects.create_user(username='owner', password='pass')
        self.other_user = UserModel.objects.create_user(username='other', password='pass')

        # Facility owned by owner
        self.facility = Facility.objects.create(name='Test Facility', owner=self.owner)

        # URLs
        self.delete_url = reverse('delete-facility', args=[self.facility.pk])
        self.success_url = reverse('facilities')
        self.fail_url = reverse('edit-facility', args=[self.facility.pk])

    def test__login_required(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test__permission_denied_for_non_owner(self):
        self.client.login(username='other', password='pass')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)

    def test__delete_successful_for_owner(self):
        self.client.login(username='owner', password='pass')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.success_url)
        self.assertFalse(Facility.objects.filter(pk=self.facility.pk).exists())

    def test__delete_blocked_if_open_or_in_progress_tickets(self):
        self.client.login(username='owner', password='pass')
        Tickets.objects.create(facility=self.facility, status='open', description='Test ticket', created_from=self.owner)

        # check if redirects to fail_url
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.fail_url)

        # Facility should still exist
        self.assertTrue(Facility.objects.filter(pk=self.facility.pk).exists())

        # Check if warning message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You cannot delete a facility that has open or in-progress tickets." in str(m) for m in messages))


class RemoveTenantViewTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(username='owner', email='owner@test.com', password='pass')
        self.tenant = UserModel.objects.create_user(username='tenant', email='tenant@test.com', password='pass')
        self.other = UserModel.objects.create_user(username='other', email='other@test.com', password='pass')

        self.facility = Facility.objects.create(
            name='Test Facility',
            owner=self.owner
        )
        self.facility.tenants.add(self.tenant)

        self.url = reverse('remove-tenant', args=[self.facility.pk])  # adjust name as needed

    def post_request(self, user, tenant_id, referer='/index/'):
        self.client.login(username=user.username, password='pass')
        return self.client.post(self.url, data={'tenant_id': tenant_id}, HTTP_REFERER=referer)

    def test__unauthenticated_post_request__redirects_to_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test__unauthorized_user_post__returns_403(self):
        self.client.login(username=self.other.username, password='pass')
        response = self.client.post(self.url, data={'tenant_id': self.tenant.id})
        self.assertEqual(response.status_code, 403)

    def test__invalid_tenant_id__raises__returns_403(self):
        request = self.post_request(self.owner, tenant_id=9999)
        self.assertEqual(request.status_code, 403)

    def test__owner_can_remove_tenant(self):
        self.post_request(self.owner, tenant_id=self.tenant.id)
        self.assertFalse(self.facility.tenants.filter(id=self.tenant.id).exists())

    def test__tenant_can_remove_themselves(self):
        response = self.post_request(self.tenant, tenant_id=self.tenant.id)
        self.assertRedirects(response, reverse('facilities'))
        self.assertFalse(self.facility.tenants.filter(id=self.tenant.id).exists())

    def test__success_url_for_owner__returns_http_referer(self):
        response = self.post_request(self.owner, tenant_id=self.tenant.id, referer='/index/')
        self.assertEqual(response.url, '/index/')

    def test__success_url_for_tenant__redirects_to_facilities(self):
        self.facility.tenants.add(self.tenant)
        response = self.post_request(self.tenant, tenant_id=self.tenant.id)
        self.assertRedirects(response, reverse('facilities'))


class EditFacilityViewTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(username='owner', password='pass')
        self.tenant = UserModel.objects.create_user(username='tenant', password='pass')
        self.other = UserModel.objects.create_user(username='other', password='pass')

        self.facility = Facility.objects.create(name='Facility 1', owner=self.owner)
        self.facility.tenants.add(self.tenant)

        self.url = reverse('edit-facility', args=[self.facility.pk])

    def test__unauthenticated_user_access__redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test__unauthorized_user_access__returns_403(self):
        self.client.login(username='other', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test__authorized_user_access__returns_200(self):
        self.client.login(username='tenant', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facilities/edit-facility.html')

    def test__context_data_includes_tenants_service_teams_owner__success(self):
        self.client.login(username='owner', password='pass')
        response = self.client.get(self.url)

        context = response.context
        self.assertIn('tenants', context)
        self.assertIn('service_teams', context)
        self.assertIn('owner', context)
        self.assertEqual(context['owner'], self.owner)

    def test__form_valid_by_unauthorized_user__returns_403(self):
        self.client.login(username='other', password='pass')
        response = self.client.post(self.url, {
            'name': 'New Name',
            'location': '',
            'postcode': '',
            'status': 'active',
            'description': ''
        })
        self.assertEqual(response.status_code, 403)

    def test__form_valid_by_owner__success(self):
        self.client.login(username='owner', password='pass')
        response = self.client.post(self.url, {
            'name': 'Updated Facility',
            'location': 'New Place',
            'postcode': '12345',
            'status': 'active',
            'description': 'Updated description',
        }, HTTP_REFERER='/facilities/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/facilities/')

        self.facility.refresh_from_db()
        self.assertEqual(self.facility.name, 'Updated Facility')

