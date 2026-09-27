from django.utils import timezone
from django.db import transaction

from celery import shared_task

import json
from datetime import datetime
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
    updates ={}
    for i in redis_keys:
        data = r.hmget(i, ["reserved_stock", "sold_stock", "status"])
        id = i.split(":")[1]
        updates[id] = {"reserved_stock":data[0],"sold_stock":data[1],"status":data[2]}

    item_to_update = list(FlashSaleItem.objects.filter(id__in=updates.keys()))
    for item in item_to_update:
        item.reserved_stock = updates[str(item.id)]['reserved_stock']
        item.sold_stock = updates[str(item.id)]["sold_stock"]
        item.status = updates[str(item.id)]["sold_stock"]

    if item_to_update:
        with transaction.atomic():
            FlashSaleItem.objects.bulk_update(
                item_to_update, fields=["reserved_stock", "sold_stock", "status"],batch_size=100
            )
