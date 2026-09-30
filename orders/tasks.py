from django.utils import timezone
from django.db import transaction
from celery import Celery

from config.redis_cache import r
from .models import Order


def check_and_change_order_status():
    now = timezone.now()
    data = Order.objects.filter(status = Order.OrderStatus.PENDING_PAYMENT,expire_date_time__lt = now)
    if data:
        for obj in data:
            obj.status = Order.OrderStatus.EXPIRED
            r.hincrby(
                name=f"FlashSaleItem:{obj.flash_sale_item.id}", key="reserved_stock",
                amount=-(obj.quantity)
            )

        with transaction.atomic():
            Order.objects.bulk_update(data,fields=['status'],batch_size=100)

        
