from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Basket, Category, Product

User = get_user_model()


class ProductsViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовое имя',
            description='Тестовое описание',
        )
        cls.product = Product.objects.create(
            name='Test name',
            description='Test description',
            price=10.5,
            quantity=1,
            image='/media/products_images/Adidas-hoodie.png',
            category=cls.category,
        )

        cls.template_use_from_reverse_url = {
            reverse('products:index'): 'products/products.html',
            reverse('products:category',
                    kwargs={'category_id': cls.category.id}): 'products/products.html',

        }

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(email='test@test.ru')
        self.client = Client()
        self.authorization = Client()
        self.authorization.force_login(self.user)

    def test_template_use_from_reverse_url(self):
        for url, template in ProductsViewTest.template_use_from_reverse_url.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)

    def test_products_list_page_show_correct_context(self):
        response = self.client.get(reverse('products:index'))
        first_obj = response.context.get('products')[0]
        product_name = first_obj.name
        product_description = first_obj.description
        product_price = first_obj.price
        product_quantity = first_obj.quantity
        product_image = first_obj.image
        product_category = first_obj.category

        self.assertEqual(product_name, 'Test name')
        self.assertEqual(product_description, 'Test description')
        self.assertEqual(product_price, 10.5)
        self.assertEqual(product_quantity, 1)
        self.assertEqual(product_image, '/media/products_images/Adidas-hoodie.png')
        self.assertEqual(product_category, self.category)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')

    def test_products_category_list_show_correct_context(self):
        response = self.client.get(reverse('products:category',
                                           kwargs={'category_id': ProductsViewTest.category.id}))
        first_obj = response.context.get('products')[0]
        product_name = first_obj.name
        product_description = first_obj.description
        product_price = first_obj.price
        product_quantity = first_obj.quantity
        product_image = first_obj.image
        product_category = first_obj.category

        self.assertEqual(product_name, 'Test name')
        self.assertEqual(product_description, 'Test description')
        self.assertEqual(product_price, 10.5)
        self.assertEqual(product_quantity, 1)
        self.assertEqual(product_image, '/media/products_images/Adidas-hoodie.png')
        self.assertEqual(product_category, self.category)


class BasketViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(email='alex@alex.ru')
        cls.category = Category.objects.create(
            name='Тестовое имя 2',
            description='Тестовое описание 2',
        )
        cls.product = Product.objects.create(
            name='Test name 2',
            description='Test description 2',
            price=5.5,
            quantity=2,
            image='/media/products_images/Adidas-hoodie.png',
            category=cls.category,
        )

    def setUp(self) -> None:
        super().setUp()
        self.authorization = Client()
        self.authorization.force_login(BasketViewTest.user)

    def test_add_basket(self):
        basket_count = Basket.objects.count()
        response = self.authorization.get(reverse('products:basket_add',
                                                  kwargs={'product_id':
                                                          self.product.id}))
        self.assertRedirects(response, reverse('products:index'))
        self.assertEqual(Basket.objects.count(), basket_count + 1)
        self.assertTrue(
            Basket.objects.filter(
                user=BasketViewTest.user,
                product=BasketViewTest.product,
            ).exists()
        )

    def test_remove_basket(self):
        self.basket = Basket.objects.create(
            user=BasketViewTest.user,
            product=BasketViewTest.product,
        )
        basket_count = Basket.objects.count()
        response = self.authorization.get(reverse('products:basket_remove',
                                                  kwargs={'basket_id':
                                                          self.basket.id}))
        self.assertRedirects(response, reverse('users:profile'))
        self.assertEqual(Basket.objects.count(), basket_count - 1)
        self.assertFalse(
            Basket.objects.filter(
                user=self.basket.user,
                product=self.basket.product,
            ).exists()
        )
