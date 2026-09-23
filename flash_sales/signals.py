from django.dispatch import receiver
from django.db.models.signals import post_save

import json
import datetime

from .models import FlashSaleItem
from config.redis_cache import r


@receiver(signal=post_save,sender=FlashSaleItem)
def auto_set_task_timer(sender,instance,created,**kwargs):
    if created:
        date_time = instance.start_date_time + datetime.timedelta(minutes=-5)
        r.zadd("flash_sale_item_scheduler",mapping={
            str(instance.id):date_time.timestamp()
        })
        r.zrange("flash_sale_item_scheduler",0,-1,withscores=True)

