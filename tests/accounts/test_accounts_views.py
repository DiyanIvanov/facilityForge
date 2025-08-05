from django.test import TestCase
from django.urls import reverse
from accounts.models import FacilityForgeUser, Team
from django.apps import apps

class DeleteTeamViewTest(TestCase):
    def setUp(self):
        self.owner = FacilityForgeUser.objects.create_user(
            username='owner', email='owner@example.com', password='TestPass'
        )
        self.non_owner = FacilityForgeUser.objects.create_user(
            username='nonowner', email='nonowner@example.com', password='TestPass'
        )
        self.member = FacilityForgeUser.objects.create_user(
            username='member', email='member@member.com', password='TestPass'
        )
        self.team = Team.objects.create(
            name='Test Team',
            team_owner=self.owner,
            manager=self.owner,
        )
        self.team.members.add(self.member)
        self.url = reverse('delete-team', kwargs={'pk': self.team.pk})

    def test__delete_team_view__redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test__delete_team_view__returns_permission_denied(self):
        self.client.login(username='nonowner', password='TestPass')
        with self.assertRaises(PermissionError):
            self.client.get(self.url)

    def test__delete_team_view__does_not_delete_team_if_team_member(self):
        self.client.login(username='member', password='TestPass')
        with self.assertRaises(PermissionError):
            self.client.get(self.url)

    def test__delete_team_view__deletes_team_if_owner(self):
        self.client.login(username='owner', password='TestPass')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('teams'))
        self.assertFalse(Team.objects.filter(pk=self.team.pk).exists())

    def test__delete_team_view__returns_404_if_team_does_not_exist(self):
        self.client.login(username='owner', password='TestPass')
        response = self.client.post(reverse('delete-team', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)


class RemoveFacilityViewTests(TestCase):
    FacilityModel = apps.get_model('facilities', 'Facility')

    def setUp(self):

        self.owner = FacilityForgeUser.objects.create_user(username='owner', email='o@test.com', password='pass')
        self.member = FacilityForgeUser.objects.create_user(username='member', email='m@test.com', password='pass')
        self.stranger = FacilityForgeUser.objects.create_user(username='stranger', email='s@test.com', password='pass')

        self.facility_owner = FacilityForgeUser.objects.create_user(username='fac_owner', email='f@test.com', password='pass')


        self.facility = self.FacilityModel.objects.create(name='Facility A', owner=self.facility_owner)

        self.team = Team.objects.create(name='Team 1', team_owner=self.owner, manager=self.owner)
        self.team.members.add(self.member)
        self.team.serviced_facilities.add(self.facility)

        self.url = reverse('remove-facility', kwargs={'pk': self.team.pk})  # adjust name if needed

    def post_request(self, user, facility_id):
        self.client.login(username=user.username, password='pass')
        return self.client.post(self.url, {'facility_id': facility_id}, HTTP_REFERER='/some-page/')

    def test__facility_not_serviced__raises_value_error(self):
        other_facility = self.FacilityModel.objects.create(name='Unrelated', owner=self.owner)
        response = None
        with self.assertRaises(ValueError):
            self.post_request(self.owner, other_facility.id)

    def test__non_member_and_non_owner__raises_permission_error(self):
        with self.assertRaises(PermissionError):
            self.post_request(self.stranger, self.facility.id)

    def test__team_owner_can_remove_facility__facility_removed(self):
        response = self.post_request(self.owner, self.facility.id)
        self.assertIn(response.status_code, [301, 302])
        self.assertNotIn(self.facility, self.team.serviced_facilities.all())

    def test__team_member_can_remove_facility__facility_removed(self):
        response = self.post_request(self.member, self.facility.id)
        self.assertIn(response.status_code, [301, 302])
        self.assertNotIn(self.facility, self.team.serviced_facilities.all())

    def test__facility_owner_can_remove_facility(self):
        response = self.post_request(self.facility_owner, self.facility.id)
        self.assertIn(response.status_code, [301, 302])
        self.assertNotIn(self.facility, self.team.serviced_facilities.all())

    def test__get_method_not_allowed__returns_405(self):
        self.client.login(username=self.owner.username, password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class RemoveMemberViewTests(TestCase):
    def setUp(self):
        self.owner = FacilityForgeUser.objects.create_user(username='owner', email='owner@test.com', password='pass')
        self.member = FacilityForgeUser.objects.create_user(username='member', email='member@test.com', password='pass')
        self.stranger = FacilityForgeUser.objects.create_user(username='stranger', email='stranger@test.com', password='pass')

        self.team = Team.objects.create(name='Test Team', team_owner=self.owner, manager=self.owner)
        self.team.members.add(self.member)

        self.url = reverse('remove-team-member', kwargs={'pk': self.team.pk})  # adjust URL name

    def post_request(self, user, member_id):
        self.client.login(username=user.username, password='pass')
        return self.client.post(self.url, {'member_id': member_id}, HTTP_REFERER='/teams/')

    def test__owner_removes_member(self):
        response = self.post_request(self.owner, self.member.id)
        self.assertRedirects(response, '/teams/')
        self.assertNotIn(self.member, self.team.members.all())

    def test__member_removes_themselves(self):
        response = self.post_request(self.member, self.member.id)
        self.assertRedirects(response, '/teams/')
        self.assertNotIn(self.member, self.team.members.all())

    def test__non_member_cannot_remove(self):
        with self.assertRaises(PermissionError):
            self.post_request(self.stranger, self.member.id)

    def test__get_method_not_allowed(self):
        self.client.login(username=self.owner.username, password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test__removing_non_member__raises_does_not_exist(self):
        with self.assertRaises(FacilityForgeUser.DoesNotExist):
            self.post_request(self.owner, 9999)

    def test__member_removes_another_member__raises_permission_error(self):
        stranger = FacilityForgeUser.objects.create_user(username='stranger', email='m2@test.com', password='pass')
        self.team.members.add(stranger)

        with self.assertRaises(PermissionError):
            self.post_request(self.member, stranger.id)

    def test__post_missing_member_id__form_invalid(self):
        self.client.login(username=self.owner.username, password='pass')
        response = self.client.post(self.url, {}, HTTP_REFERER='/teams/')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'member_id', 'This field is required.')

    def test__anonymous_user_access__redirects_to_login(self):
        response = self.client.post(self.url, {'member_id': self.member.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


class EditTeamViewTests(TestCase):
    FacilityModel = apps.get_model('facilities', 'Facility')

    def setUp(self):
        self.owner = FacilityForgeUser.objects.create_user(username='owner', email='owner@test.com', password='pass')
        self.member = FacilityForgeUser.objects.create_user(username='member', email='member@test.com', password='pass')
        self.stranger = FacilityForgeUser.objects.create_user(username='stranger', email='stranger@test.com', password='pass')

        self.facility = self.FacilityModel.objects.create(name='Facility A', owner=self.owner)

        self.team = Team.objects.create(
            name='Test Team',
            description='Initial description',
            moto='Initial motto',
            team_owner=self.owner,
            manager=self.owner
        )
        self.team.members.add(self.member)
        self.team.serviced_facilities.add(self.facility)

        self.url = reverse('edit-team', kwargs={'pk': self.team.pk})

    def post_request(self, user, data):
        self.client.login(username=user.username, password='pass')
        return self.client.post(self.url, data, HTTP_REFERER='/teams/')

    def test__owner_can_access_edit_page__returns_200(self):
        self.client.login(username=self.owner.username, password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test__team_member_can_access_edit_page__returns_200(self):
        self.client.login(username=self.member.username, password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test__non_member_access_edit_page__raises_permission_error(self):
        self.client.login(username=self.stranger.username, password='pass')
        with self.assertRaises(PermissionError):
            self.client.get(self.url)

    def test__owner_can_submit_changes__form_saved(self):
        self.client.login(username=self.owner.username, password='pass')
        data = {
            'name': 'Updated Team Name',
            'description': 'Updated description',
            'moto': 'Updated motto',
            'members': [self.member.id],
            'serviced_facilities': [self.facility.id]
        }
        response = self.post_request(self.owner, data)
        self.assertRedirects(response, '/teams/')
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'Updated Team Name')
        self.assertEqual(self.team.description, 'Updated description')
        self.assertEqual(self.team.moto, 'Updated motto')
        self.assertIn(self.member, self.team.members.all())
        self.assertIn(self.facility, self.team.serviced_facilities.all())

    def test__member_cannot_submit_changes__raises_permission_error(self):
        self.client.login(username=self.member.username, password='pass')
        data = {
            'name': 'Updated Team Name',
            'description': 'Updated description',
            'moto': 'Updated motto',
            'members': [self.member.id],
            'serviced_facilities': [self.facility.id]
        }
        with self.assertRaises(PermissionError):
            self.post_request(self.member, data)

    def test__non_member_cannot_submit_changes__raises_permission_error(self):
        self.client.login(username=self.stranger.username, password='pass')
        data = {
            'name': 'Updated Team Name',
            'description': 'Updated description',
            'moto': 'Updated motto',
            'members': [self.member.id],
            'serviced_facilities': [self.facility.id]
        }
        with self.assertRaises(PermissionError):
            self.post_request(self.stranger, data)

    def test__context_data_contains_expected_keys__context_correct(self):
        self.client.login(username=self.owner.username, password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('form', context)
        self.assertIn('team_owner', context)
        self.assertIn('team_members', context)
        self.assertIn('facilities', context)
        self.assertEqual(context['team_owner'], self.team.team_owner)
        self.assertIn(self.member, context['team_members'])
        self.assertIn(self.facility, context['facilities'])


class CreateTeamViewTests(TestCase):
    def setUp(self):
        self.user = FacilityForgeUser.objects.create_user(
            username='testuser', email='test@example.com', password='pass'
        )
        self.url = reverse('create-team')

    def test__unauthenticated_user_access__redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test__authenticated_user_get_request__returns_200(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/create-team.html')

    def test__authenticated_user_post_request__creates_team(self):
        self.client.login(username=self.user.username, password='pass')
        data = {
            'name': 'New Team',
            'description': 'A new team description',
            'moto': 'Team moto',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('teams'))

        team = Team.objects.get(name='New Team')
        self.assertEqual(team.description, 'A new team description')
        self.assertEqual(team.moto, 'Team moto')

    def test__team_owner_set_correctly__team_owner_is_user(self):
        self.client.login(username='testuser', password='pass')
        data = {
            'name': 'New Team',
            'description': 'A new team description',
            'moto': 'Team moto',
            'members': [self.user.id],
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('teams'))
        team = Team.objects.get(name='New Team')
        self.assertEqual(team.team_owner, self.user)
        self.assertEqual(team.manager, self.user)

