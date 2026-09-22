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
# time_list = [(1,4),(2,5),(3,1),(4,2),(5,10)]
# for pair in time_list:
#     time =past_time + datetime.timedelta(minutes=pair[1])
#     r.zadd(
#         "tasks_date",
#         mapping={
#             pair[0]: time.timestamp()  ,
#         },
#     )

now= datetime.datetime.now()
xyz = r.zrevrangebyscore("tasks_date", min=0, max=now.timestamp(), withscores=True)
print(xyz)

print((xyz[0][0], datetime.datetime.fromtimestamp(xyz[0][1])) if xyz else None)
