from redis import Redis
from rq import Worker, Queue
# RQ needs a worker process running separately.
# overall procedure needed: make requests async using a queue
redis_conn = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

queue = Queue("chat_jobs", connection=redis_conn)
worker = Worker([queue], connection=redis_conn)
worker.work()