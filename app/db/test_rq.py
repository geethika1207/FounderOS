from redis import Redis
from rq import Queue

redis_conn = Redis(
    host="localhost",
    port=6379
)

queue = Queue(connection=redis_conn)

def say_hello(name):
    print(f"Hello {name}")
    return f"Hello {name}"

job = queue.enqueue(
    say_hello,
    "Geethika"
)

print(job.id)