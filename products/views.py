from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import Category, Product, Basket


LIMIT_PAGE: int = 3


def func_paginator(request, queryset):
    paginator = Paginator(queryset, LIMIT_PAGE)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return page_obj


def home(request):
    return render(request, 'products/home.html')


def products(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = category.products.all()
        page_obj = func_paginator(request, products)
    else:
        products = Product.objects.all()
        page_obj = func_paginator(request, products)
    context = {'page_obj': page_obj,
               'categories': categories}

    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])