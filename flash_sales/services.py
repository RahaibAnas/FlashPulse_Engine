from datetime import datetime
from .models import FlashSaleItem
from config.redis_cache import r

def cache_flash_item(id_list:list):
    id_list = ['b212f2d8-4632-44ea-af46-bdcc2965e88e']
    sale_item_data = FlashSaleItem.objects.filter(id__in = id_list).values()
    for obj in sale_item_data:
        redis_key_name = "FlashSaleItem:{obj.get('id')}"
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


# <QuerySet [{'id': UUID('b212f2d8-4632-44ea-af46-bdcc2965e88e'), 'product_id': UUID('0a90b9ff-7abd-4aac-8a30-ec0cbdc97397'), 'flash_price': Decimal('12.00'), 'allocate_stock': 9, 'reserved_stock': 0, 'sold_stock': 0, 'start_date_time': datetime.datetime(2026, 9, 23, 2, 20, 47, tzinfo=datetime.timezone.utc), 'end_date_time': datetime.datetime(2026, 9, 23, 13, 0, tzinfo=datetime.timezone.utc), 'status': 'ACTIVE', 'created_at': datetime.datetime(2026, 9, 23, 2, 11, 59, 565338, tzinfo=datetime.timezone.utc)}]>
