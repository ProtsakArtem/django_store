from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CancelTemplateView, payment_return
from users.views import RegisterView, ProfileView, LoginFormView, EmailVerificationView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CancelTemplateView.as_view(), name='order_canceled'),
    path('payment-return/', payment_return, name='payment_return'),
]