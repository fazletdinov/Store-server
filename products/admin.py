from django.contrib import admin

from .models import Basket, Category, Product, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class CommentAdmin(admin.TabularInline):
    model = Comment
    fields = ('id', 'product', 'author', 'text', 'created')
    readonly_fields = ('created',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    fields = ('name', 'author', 'description', ('price', 'quantity'),
              ('image', 'file'), 'stripe_product_price_id', 'category', 'created_book')
    readonly_fields = ('created_book',)
    inlines = (CommentAdmin,)
    search_fields = ('name',)
    list_display_links = ('name',)
    list_filter = ('category',)
    list_editable = ('category',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
