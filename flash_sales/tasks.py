from django.utils import timezone

from celery import shared_task

import json
from datetime import datetime

from .models import FlashSaleItem
from config.redis_cache import r



@shared_task
def sale_pre_warming():
    flash_sale_scheduler = r.lrange("flash_sale_item_scheduler",0,-1)
    if flash_sale_scheduler:
        for key in range(len(flash_sale_scheduler)):
            d = json.loads(flash_sale_scheduler[key])
            start_time = datetime.isoformat(d.get('start_date_time'))
            if timezone.now() >= start_time:
                FlashSaleItem.objects.filter(id = d.get('id')).update(status=FlashSaleItem.SaleStatus.ACTIVE)
                flash_sale_scheduler.pop(key)
