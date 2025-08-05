from django.test import TestCase
from django.contrib.auth import get_user_model
from facilities.models import Facility
from accounts.models import Team

UserModel = get_user_model()

class FacilityManagerTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='Owner', email='owner@test.com', password='pass')
        self.other_user = UserModel.objects.create_user(username='user', email='user@test.com', password='pass')

        self.user_team = Team.objects.create(name="OwnerTeam", team_owner=self.user, manager=self.user)
        self.other_team = Team.objects.create(name="OtherTeam", team_owner=self.other_user, manager=self.other_user)

        self.owned_facility = Facility.objects.create(name="OwnedFacility", owner=self.user)
        self.managed_facility = Facility.objects.create(name="ManagedFacility", owner=self.other_user, manager=self.user)

        self.tenant_facility = Facility.objects.create(name="TenantFacility", owner=self.other_user)
        self.tenant_facility.tenants.add(self.user)

        self.teamed_facility = Facility.objects.create(name="TeamedFacility", owner=self.other_user)
        self.teamed_facility.engineering_teams.add(self.user_team)

        self.unrelated_facility = Facility.objects.create(name="UnrelatedFacility", owner=self.other_user)

    def test__facilities_user_is_involved_in__returns_related_facilities(self):
        involved = Facility.objects.facilities_user_is_involved_in(self.user)
        names = {f.name for f in involved}

        expected = {"OwnedFacility", "ManagedFacility", "TeamedFacility", "TenantFacility"}
        self.assertEqual(names, expected)

    def test__facilities_user_is_not_involved_in__excludes_related_facilities(self):
        uninvolved = Facility.objects.facilities_user_is_not_involved_in(self.user)
        names = {f.name for f in uninvolved}

        self.assertEqual(names, {"UnrelatedFacility"})
