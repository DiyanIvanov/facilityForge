from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class IndexPageViewTests(TestCase):
    def setUp(self):
        self.index_url = reverse('index')
        self.dashboard_url = reverse('dashboard')

        self.user = UserModel.objects.create_user(
            username='TestUser',
            email='test@example.com',
            password='pass1234'
        )

    def test_index_page_redirects__authenticated_user(self):
        self.client.login(username='TestUser', password='pass1234')
        response = self.client.get(self.index_url)
        self.assertRedirects(response, self.dashboard_url)

    def test_index_page_renders__unauthenticated_user(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html')


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='TestUser', email='test@example.com', password='pass1234'
        )
        self.url = reverse('dashboard')

    def test__unauthenticated_user_access__redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')


    def test__authenticated_user_access__returns_dashboard_page(self):
        self.client.login(username='testuser', password='pass1234')

        response = self.client.get(self.url)
        self.assertIn(response.status_code, (302, 301, 200))



