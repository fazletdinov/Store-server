from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersTestUrls(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(email='test@test.ru')

        cls.url_status_code_client = {
            reverse('users:login'): HTTPStatus.OK,
            reverse('users:signup'): HTTPStatus.OK,
            reverse('users:profile'): HTTPStatus.FOUND,
            reverse('users:logout'): HTTPStatus.FOUND,
        }

        cls.template_use_client = {
            reverse('users:login'): 'users/login.html',
            reverse('users:signup'): 'users/signup.html',
        }

        cls.redirect_url_client = {
            reverse('users:profile'): reverse('users:login') + '?next=' + reverse('users:profile'),
            reverse('users:logout'): reverse('home')
        }

        cls.url_status_code_autherization_client = {
            reverse('users:login'): HTTPStatus.OK,
            reverse('users:signup'): HTTPStatus.OK,
            reverse('users:profile'): HTTPStatus.OK,
            reverse('users:logout'): HTTPStatus.FOUND,
        }

    def setUp(self):
        self.authorization_client = Client()
        self.authorization_client.force_login(self.user)

    def test_url_status_code_client(self):
        for url, status in self.url_status_code_client.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_template_use_client(self):
        for url, template in self.template_use_client.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)

    def test_redirect_url_client(self):
        for url, redirect in self.redirect_url_client.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect)

    def test_url_status_code_authorization_client(self):
        for url, status in self.url_status_code_autherization_client.items():
            with self.subTest(url=url):
                response = self.authorization_client.get(url)
                self.assertEqual(response.status_code, status)
