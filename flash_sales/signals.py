from django.dispatch import receiver
from django.db.models.signals import post_save

import json
import datetime

from .models import FlashSaleItem
from config.redis_cache import r


@receiver(signal=post_save,sender=FlashSaleItem)
def auto_set_task_timer(sender,instance,created,**kwargs):
    if created:
        start_date_time = instance.start_date_time + datetime.timedelta(minutes=-3)
        end_date_time = instance.end_date_time
        r.zadd("flash_sale_item_scheduler",mapping={
            str(instance.id):start_date_time.timestamp()
        })

        r.zadd('flash_sale_end_time_scheduler',mapping={
            str(instance.id): end_date_time.timestamp()
        })

