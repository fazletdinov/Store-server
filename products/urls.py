from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.PoductListView.as_view(), name='index'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/downloads/', views.download_file, name='download_file'),
    path('<int:product_id>/comments/', views.add_comment, name='add_comments'),
    path('category/<int:category_id>/', views.PoductListView.as_view(),
         name='category'),
    path('baskets/add/<int:product_id>/', views.basket_add,
         name='basket_add'),
    path('basket/remove/<int:basket_id>/', views.basket_remove,
         name='basket_remove'),
]
