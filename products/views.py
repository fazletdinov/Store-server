from django.shortcuts import render, get_object_or_404, redirect

from products.models import Category, Product, Basket


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


def basket_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product_id)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return redirect(request.META['HTTP_REFERER'])
