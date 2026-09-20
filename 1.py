import redis
import json

r = redis.Redis(host="localhost", port="6379", db=2, decode_responses=True)
r.delete('task')

a= {"id":123,"date":"qw"}
b = {"id": 123, "date": "wq"}
c = {"id": 123, "date": "qw"}
d = {"id": 123, "date": "wq"}


r.rpush("task",json.dumps(a))
r.rpush("task",json.dumps(b))
r.rpush("task",json.dumps(c))
r.rpush("task",json.dumps(d))
li = r.lrange("task", 0, -1)
for i in range(len(li)):
    a =json.loads(li[i])
    print(a.get('id'),a.get('date'))
    
