from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('order-create/', views.OderCreateView.as_view(), name='order_create'),
    path('order-success/', views.SuccessTemplateView.as_view(), name='order_success'),
    path('order-cancel/', views.CancelTemplateView.as_view(), name='order_cancel'),

]