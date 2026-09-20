from django.dispatch import receiver
from django.db.models.signals import post_save
import json
from datetime import timedelta

from .models import FlashSaleItem
from config.redis_cache import r


@receiver(signal=post_save,sender=FlashSaleItem)
def auto_set_task_timer(sender,instance,created,*kwargs):
    if created:
        dic = {"id":instance.id,"start_date_time":instance.start_date - timedelta(minutes=5) }
        r.rpush('flash_sale_item_scheduler',json.dumps(dic))
