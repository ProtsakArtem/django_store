from django.urls import path
from orders.views import OrderCreateView, SuccessTemplateView, CancelTemplateView, payment_return, OrderListView, \
    OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CancelTemplateView.as_view(), name='order_canceled'),
    path('payment-return/', payment_return, name='payment_return'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),
]