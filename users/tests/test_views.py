from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification

User = get_user_model()


class SignUpViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('users:signup')
        self.redirect_url = reverse('users:login')
        self.from_data = {
            'email': 'alex@alex.ru',
            'phone': '12345678910',
            'password': 'alex12345',
        }

    def test_signup_post(self):
        self.assertFalse(User.objects.filter(
            email=self.from_data['email'],
            phone=self.from_data['phone'],
        ).exists())
        response = self.client.post(self.url, data=self.from_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_url)
        self.assertTrue(
            User.objects.filter(
                email=self.from_data['email'],
                phone=self.from_data['phone'],
            ).exists()
        )
        self.email_verification = EmailVerification.objects.filter(user__email=self.from_data['email'])
        self.assertTrue(self.email_verification.exists())
        self.assertEqual(
            self.email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_signup_error(self):
        User.objects.create(email=self.from_data['email'])
        response = self.client.post(self.url, data=self.from_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким Email уже существует.', html=True)
