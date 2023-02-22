from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.urls import reverse, resolve

from ..models import Product, Category, Basket

User = get_user_model()


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

    def setUp(self) -> None:
        super().setUp()
        self.authentication_user = Client()
        self.authentication_user.force_login(ProductUrlsTest.author)

    def test_product_urls_status_code(self):
        url_status_code = {
            '/products/': HTTPStatus.OK,
            f'/products/category/{self.category.id}/': HTTPStatus.OK,
        }

        for url, status_code_use in url_status_code.items():
            with self.subTest(url=url):
                response = self.authentication_user.get(url)
                self.assertEqual(response.status_code, status_code_use)

    def test_urls_status_core_redirect(self):
        url_status_code = {
            f'/products/baskets/add/{self.product.id}/':
            reverse('products:index'),
            f'/products/basket/remove/{self.basket.id}/':
            reverse('users:profile'),
        }

        for url, redirect_url in url_status_code.items():
            with self.subTest(url=url):
                response = self.authentication_user.get(url)
                self.assertRedirects(response, redirect_url)