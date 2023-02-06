from django.shortcuts import render

from products.models import Category, Product


def index(request):
    context = {
        'title': 'Test title',
        'username': 'Valeryia'
    }
    return render(request, 'products/index.html', context=context)


def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {'products': products,
               'categories': categories}

    return render(request, 'products/products.html', context)
