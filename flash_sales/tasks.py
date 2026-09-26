from django.utils import timezone

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
    events = r.zrangebyscore("flash_sale_end_time_schedular",min=0,max=now.timestamp(),withscores=True)
    event_ids  =[]
    if events:
        for pair in events:
            event_ids.append(UUID(pair[0]))
            r.zrem("flash_sale_end_time_schedular",pair[0])
        FlashSaleItem.objects.filter(id__in = event_ids).update(status=FlashSaleItem.SaleStatus.ENDED)

    
