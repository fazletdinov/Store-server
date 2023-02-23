from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='products')

    def __str__(self) -> str:
        return f"Продукт: {self.name} | Категория: {self.category.name}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='baskets')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE,
                                related_name='products')
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self) -> str:
        return f"Корзина для {self.user.email} | Корзина {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price
    
