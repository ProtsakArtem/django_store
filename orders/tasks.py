from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from orders.wayforpay_integration.wfp import WayForPay
from orders.models import Order
import time

@shared_task(bind=True, max_retries=180)
def check_invoice_status(self, order_reference, order_id, created_time):
    wayforpay = WayForPay(key=settings.WFP_KEY, domain_name="mvg_restart_ssd_space")
    result = wayforpay.check_invoice(
        merchantAccount="mvg_restart_ssd_space",
        orderReference=order_reference
    )
    created_time = datetime.fromisoformat(created_time)
    if hasattr(result, 'reasonCode') and result.reasonCode == 1100:
        order = Order.objects.get(pk=order_id)
        order.status = Order.PAID
        order.save()
        fulfill_order(order)
        return True
    elif datetime.now() < (created_time + timedelta(hours=3)):
        raise self.retry(countdown=60)
    return False


def fulfill_order(order):
    order.update_after_payment()
