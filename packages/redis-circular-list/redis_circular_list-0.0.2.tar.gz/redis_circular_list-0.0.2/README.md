# Redis Circular List

```
python3 -m pip install redis-circular-list
```

```
import redis
import redis_circular_list

redis_connection = redis.StrictRedis(
	host="127.0.0.1" ,
	port="6379" ,
	db=1 ,
	)

next_in_circular_list = redis_circular_list.next( redis_connection , "LIST_KEY" )
previous_in_circular_list = redis_circular_list.previous( redis_connection , "LIST_KEY" )
```