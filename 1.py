# from flash_sales.models import FlashSaleItem
# from config.redis_cache import r

import redis
import json
import datetime

r = redis.Redis(host="localhost", port="6379", db=2, decode_responses=True)
r.delete('task')

# a= {"id":123,"date":datetime.datetime.now()+datetime.timedelta(minutes=4)}
# b = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=3)}
# c = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=6)}
# d = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=1)}
# e = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=1)}
# f = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=1)}

# r.delete("tasks_date")
# past_time = datetime.datetime.now()+datetime.timedelta(minutes=-5)
# time_list = [(1,4),(2,6),(3,3),(4,6),(5,10)]
# for pair in time_list:
#     time =past_time + datetime.timedelta(minutes=pair[1])
#     r.zadd(
#         "flash_sale_item_scheduler",
#         mapping={
#             pair[0]: time.timestamp()  ,
#         },
#     )

# now= datetime.datetime.now()
# max_time = now.timestamp()
# xyz = r.zrangebyscore("flash_sale_item_scheduler", min=0, max=max_time, withscores=True)
# print(xyz)

# print(max_time)

# print((xyz[0][0], datetime.datetime.fromtimestamp(xyz[0][1])) if xyz else None)
# 1790129367
# print(datetime.datetime.fromtimestamp(1790129747))


def cache_flash_item():
    id_list = ["b212f2d8-4632-44ea-af46-bdcc2965e88e"]
    # data = FlashSaleItem.objects.filter(id__in=id_list).values()
    # print(data)


# <QuerySet [{'id': UUID('b212f2d8-4632-44ea-af46-bdcc2965e88e'), 'product_id': UUID('0a90b9ff-7abd-4aac-8a30-ec0cbdc97397'), 'flash_price': Decimal('12.00'), 'allocate_stock': 9, 'reserved_stock': 0, 'sold_stock': 0, 'start_date_time': datetime.datetime(2026, 9, 23, 2, 20, 47, tzinfo=datetime.timezone.utc), 'end_date_time': datetime.datetime(2026, 9, 23, 13, 0, tzinfo=datetime.timezone.utc), 'status': 'ACTIVE', 'created_at': datetime.datetime(2026, 9, 23, 2, 11, 59, 565338, tzinfo=datetime.timezone.utc)}]>
