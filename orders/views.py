from datetime import datetime
import logging
from django.shortcuts import redirect, render
from orders.models import Order
from orders.tasks import check_invoice_status
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from orders.forms import OrderForm
from common.views import TitleMixin
from django.conf import settings
from orders.wayforpay_integration.wfp import WayForPay
logger = logging.getLogger(__name__)

class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = "Store - Заказ успішно здійснено"


class CancelTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = "Store - Замовлення відмінено"


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = "Store - Мої замовлення"
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Store - заказ #{self.object.id}"
        return context


class OrderCreateView(TitleMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order-create.html'
    title = 'Store - Оформлення замовлення'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            order = form.save(commit=False)
            order.initiator = request.user
            order.save()

            carts = request.user.cart_set.all()
            product_names = [cart.product.name for cart in carts]
            product_prices = [int(cart.product.price) for cart in carts]
            product_counts = [cart.quantity for cart in carts]
            amount = sum(cart.product.price * cart.quantity for cart in carts)

            wayforpay = WayForPay(key=settings.WFP_KEY, domain_name="mvg_restart_ssd_space")
            result = wayforpay.create_invoice(
                merchantAccount="mvg_restart_ssd_space",
                merchantAuthType='SimpleSignature',
                amount=int(amount),
                currency='UAH',
                productNames=product_names,
                productPrices=product_prices,
                productCounts=product_counts,
                service_url=f"{settings.DOMAIN_NAME}{reverse('orders:payment_return')}",
            )
            if hasattr(result, 'invoiceUrl'):
                check_invoice_status.apply_async((result.orderReference, order.id, datetime.now().isoformat()))

                return redirect(result.invoiceUrl)
            else:
                form.add_error(None, 'Error generating payment link')
                return self.form_invalid(form)


def payment_return(request):
    logger.info("Повернення від WayForPay отримано")
    logger.info(f"Дані запиту: {request.GET}")

    order_id = request.GET.get('orderReference')
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.status = Order.PAID
            order.save()
            return render(request, 'orders/success.html', {'order': order})
    return HttpResponseRedirect('/error/')
