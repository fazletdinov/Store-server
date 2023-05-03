from django.contrib.auth import get_user_model
from django.test import TestCase

from products.models import Basket, Category, Product

User = get_user_model()


class ProductsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(email='test@test.ru')
        cls.category = Category.objects.create(
            name='Тестовое наименование',
            description='Тестовое описание',
        )
        cls.product = Product.objects.create(
            name='Наименование продукта',
            description='Описание продукта',
            price=24.5,
            category=cls.category,
        )
        cls.basket = Basket.objects.create(
            user=cls.author,
            product=cls.product,
            quantity=5,
        )

        cls.product2 = Product.objects.create(
            name='Наименование продукта 2',
            description='Описание продукта 2',
            price=20.5,
            category=cls.category,
        )

        cls.basket2 = Basket.objects.create(
            user=cls.author,
            product=cls.product2,
            quantity=10,
        )

    def setUp(self) -> None:
        self.str_product = f"Продукт: {self.product.name} | Категория: {self.category.name}"
        self.str_category = self.category.name
        self.str_basket = f"Корзина для {self.basket.user.email} | Корзина {self.category.name}"
        self.sum_quantity_and_price = 5 * 24.5
        self.total_sum_test = (5 * 24.5) + (10 * 20.5)
        self.total_quantity_test = 5 + 10

    def test_str_product_basket_category(self):
        product = ProductsModelTest.product
        category = ProductsModelTest.category
        basket = ProductsModelTest.basket
        self.assertEqual(self.str_product, str(product))
        self.assertEqual(self.str_category, str(category))
        self.assertEqual(self.str_basket, str(basket))

    def test_sum_method_basket(self):
        basket = Basket.objects.first()
        self.assertEqual(self.sum_quantity_and_price, basket.sum())

    def test_totul_sum_basket(self):
        baskets = Basket.objects.all()
        self.assertEqual(self.total_sum_test, baskets.total_sum())

    def test_total_quantity(self):
        baskets = Basket.objects.all()
        self.assertEqual(self.total_quantity_test, baskets.total_quantity())
