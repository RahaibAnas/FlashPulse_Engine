from django.utils import timezone
from django.db import transaction

from celery import shared_task
from uuid import UUID

from .models import FlashSaleItem
from config.redis_cache import r
from .services import cache_flash_item


@shared_task
def sale_pre_warming():
    now = timezone.now()
    events = r.zrangebyscore(
        "flash_sale_item_scheduler", min=0, max=now.timestamp(), withscores=True
    )
    if events:
        event_ids = []
        for pair in events:
            event_ids.append(UUID(pair[0]))
            r.zrem("flash_sale_item_scheduler", pair[0])
        FlashSaleItem.objects.filter(id__in = event_ids).update(status=FlashSaleItem.SaleStatus.ACTIVE)
        cache_flash_item(event_ids)


@shared_task
def item_sale_ender():
    now = timezone.now()
    events = r.zrangebyscore(
        "flash_sale_end_time_scheduler", min=0, max=now.timestamp(), withscores=True
    )
    event_ids  =[]
    if events:
        for pair in events:
            event_ids.append(UUID(pair[0]))
            r.zrem("flash_sale_end_time_scheduler", pair[0])
        FlashSaleItem.objects.filter(id__in = event_ids).update(status=FlashSaleItem.SaleStatus.ENDED)

@shared_task
def sync_redis_to_postgres():
    redis_keys = r.keys("FlashSaleItem:*")
    if not redis_keys:
        return
    key_id_list = []
    for i in redis_keys:
        id = i.split(":")[1]
        key_id_list.append(id)

    item_to_update = list(FlashSaleItem.objects.filter(id__in=key_id_list))
    for item in item_to_update:
        key = f"FlashSaleItem:{item.id}"
        key_data = r.hmget(key, ["reserved_stock", "sold_stock", "status"])
        item.reserved_stock = key_data[0]
        item.sold_stock = key_data[1]
        item.status = key_data[2]

    if item_to_update:
        with transaction.atomic():
            FlashSaleItem.objects.bulk_update(
                item_to_update, fields=["reserved_stock", "sold_stock", "status"],batch_size=100
            )
