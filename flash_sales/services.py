from datetime import datetime
from .models import FlashSaleItem
from config.redis_cache import r

def cache_flash_item(id_list:list):
    sale_item_data = FlashSaleItem.objects.filter(id__in = id_list).values()
    for obj in sale_item_data:
        redis_key_name = f"FlashSaleItem:{obj.get('id')}"
        mapping={
            "flash_price":float(obj.get('flash_price')),
            "allocate_stock": obj.get("allocate_stock"),
            "reserved_stock": obj.get('reserved_stock'),
            "sold_stock": obj.get('sold_stock'),
            'status':obj.get('status')
        }
        start = obj.get('start_date_time')
        end = obj.get('end_date_time')
        mapping["start_date_time"] = datetime.isoformat(start)
        mapping["end_date_time"] = datetime.isoformat(end)

        r.hset(name=redis_key_name,mapping=mapping)

        print(f"item cashe successfully {obj.get('id')}")

def sale_end_date_time_set(id_list:list):
    pass


