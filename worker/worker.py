from redis import Redis
from rq import Worker, Queue, connections

listen = ["chat_jobs"]

# RQ needs a worker process running separately.
# overall procedure needed: make requests async using a queue
redis_conn = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

if __name__ == "__main__":
    with connections(redis_conn):
        worker = Worker([Queue(name) for name in listen])
        worker.work()
