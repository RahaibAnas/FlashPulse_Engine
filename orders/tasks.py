from django.utils import timezone
from django.db import transaction
from celery import shared_task

from config.redis_cache import r
from .models import Order


@shared_task
def check_and_change_order_status():
    now = timezone.now()
    data = Order.objects.filter(
        status=Order.OrderStatus.PENDING_PAYMENT, expires_at__lt=now
    )
    if data:
        for obj in data:
            obj.status = Order.OrderStatus.EXPIRED
            if r.hexists(
                name=f"FlashSaleItem:{obj.flash_sale_item.id}", key="reserved_stock"
            ):
                r.hincrby(
                    name=f"FlashSaleItem:{obj.flash_sale_item.id}",
                    key="reserved_stock",
                    amount=-(obj.quantity),
                )

        with transaction.atomic():
            Order.objects.bulk_update(data, fields=["status"], batch_size=100)
