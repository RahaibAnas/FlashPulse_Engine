# from flash_sales.models import FlashSaleItem
# from config.redis_cache import r

import redis
import json
import datetime

r = redis.Redis(host="localhost", port="6379", db=2, decode_responses=True)
# r.delete('task')

# a= {"id":123,"date":datetime.datetime.now()+datetime.timedelta(minutes=4)}
# b = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=3)}
# c = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=6)}
# d = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=1)}
# e = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=1)}
# f = {"id": 123, "date": datetime.datetime.now() + datetime.timedelta(minutes=1)}


# li = r.keys("FlashSaleItem:*")
# for i in li:
#     h = r.hgetall(i)
#     print(h)

# redis_keys = r.keys("FlashSaleItem:*")

# updates ={}
# for i in redis_keys:
#     print(i.split(":")[1])
#     a = r.hmget(i,['reserved_stock','sold_stock','status'])
#     print(a)


d = list({'a':123})
# print(d)
print(list(d))


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


# def cache_flash_item():
#     id_list = ["b212f2d8-4632-44ea-af46-bdcc2965e88e"]
# data = FlashSaleItem.objects.filter(id__in=id_list).values()
# print(data)


# <QuerySet [{'id': UUID('b212f2d8-4632-44ea-af46-bdcc2965e88e'), 'product_id': UUID('0a90b9ff-7abd-4aac-8a30-ec0cbdc97397'), 'flash_price': Decimal('12.00'), 'allocate_stock': 9, 'reserved_stock': 0, 'sold_stock': 0, 'start_date_time': datetime.datetime(2026, 9, 23, 2, 20, 47, tzinfo=datetime.timezone.utc), 'end_date_time': datetime.datetime(2026, 9, 23, 13, 0, tzinfo=datetime.timezone.utc), 'status': 'ACTIVE', 'created_at': datetime.datetime(2026, 9, 23, 2, 11, 59, 565338, tzinfo=datetime.timezone.utc)}]>


{"email": "meer@gmail.com", "password": "Meer1234"}

{
    "flash_sale_item": "9380f860-0e2b-497d-b37f-28d79c98857c",
    "quantity": 6,
    "idempotency_key": "12321",
}

{
    "success": true,
    "message": "the order is proceed successfully.you have five minutes to pay this",
    "data": {
        "id": "1f6337e7-dcbd-475b-be0d-1a011f4990a7",
        "quantity": 2,
        "total_amount": "20.00",
        "status": "PENDING_PAYMENT",
        "idempotency_key": "12321",
        "expires_at": "2026-10-02T10:02:55.678471+05:00",
        "created_at": "2026-10-02T10:09:21.238098+05:00",
        "updated_at": "2026-10-02T10:09:21.238213+05:00",
        "user": "d83a7fb1-160a-4e91-98b5-c1d88860a54e",
        "flash_sale_item": "e1ab9a82-dfb6-443c-9510-c60fb28117be",
    },
}


