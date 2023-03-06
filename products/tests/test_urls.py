from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Basket, Category, Product

User = get_user_model()


class HomeUrlTest(TestCase):
    def test_url_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/home.html')
        self.assertEqual(response.context.get('title'), 'Store')


class ProductUrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(email='test@test.ru')
        cls.category = Category.objects.create(name='Тест категория')
        cls.product = Product.objects.create(
            name='Тест продукт',
            category=cls.category,
            price=23.56,
            image='/media/products_images/Adidas-hoodie.png'
        )
        cls.basket = Basket.objects.create(
            user=cls.author,
            product=cls.product,
        )

        cls.url_status_code = {
            '/products/': HTTPStatus.OK,
            f'/products/category/{cls.category.id}/': HTTPStatus.OK,
        }

        cls.url_redirect_authentication_user = {
            f'/products/baskets/add/{cls.product.id}/':
                reverse('products:index'),
            f'/products/basket/remove/{cls.basket.id}/':
                reverse('users:profile'),
        }

        cls.url_redirect_unauthentication_user = {
            f'/products/baskets/add/{cls.product.id}/':
                reverse('users:login') + f'?next=/products/baskets/add/{cls.product.id}/',
            f'/products/basket/remove/{cls.basket.id}/':
                reverse('users:login') + f'?next=/products/basket/remove/{cls.basket.id}/',
        }

        cls.url_tamplate_use = {
            '/products/': 'products/products.html',
            f'/products/category/{cls.category.id}/': 'products/products.html',

        }

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.authentication_user = Client()
        self.authentication_user.force_login(ProductUrlsTest.author)

    def test_product_urls_status_code_authentication_user(self):

        for url, status_code_use in ProductUrlsTest.url_status_code.items():
            with self.subTest(url=url):
                response = self.authentication_user.get(url)
                self.assertEqual(response.status_code, status_code_use)

    def test_product_urls_status_code_unauthentication_user(self):
        for url, status_code_use in ProductUrlsTest.url_status_code.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status_code_use)

    def test_urls_redirect_authentication_user(self):

        for url, redirect_url in ProductUrlsTest.url_redirect_authentication_user.items():
            with self.subTest(url=url):
                response = self.authentication_user.get(url)
                self.assertRedirects(response, redirect_url)

    def test_urls_redirect_unauthentication_user(self):

        for url, redirect_url in ProductUrlsTest.url_redirect_unauthentication_user.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_use_template_unauthentication_user(self):

        for url, template in ProductUrlsTest.url_tamplate_use.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)
