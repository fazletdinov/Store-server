from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView
from django.core.cache import cache
from django.http import FileResponse

from core.mixins.mixin import TitleMixin
from products.models import Basket, Category, Product
from .forms import CommentForm

LIMIT_PAGE: int = 3


@login_required
def download_file(request, product_id):
    product = Product.objects.get(id=product_id)
    filename = product.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


class HomeView(TitleMixin, TemplateView):
    template_name = 'products/home.html'
    title = 'Store-Book'


class PoductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = LIMIT_PAGE
    title = 'Store-Book - Каталог'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.select_related().filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories = cache.get('categories')
        if not categories:
            context['categories'] = Category.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()
    form = CommentForm()

    context = {
        "product": product,
        "comments": comments,
        "form": form,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def basket_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    baskets = Basket.objects.select_related('user', 'product').filter(
        user=request.user, product=product
    )

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return redirect('products:index')


@login_required
def basket_remove(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    basket.delete()
    return redirect('users:profile')


@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CommentForm(data=request.POST or None)
    if form.is_valid():
        comment_form = form.save(commit=False)
        comment_form.author = request.user
        comment_form.product = product
        comment_form.save()
    return redirect('products:product_detail', product_id=product_id)



