import os
from urllib.parse import urlparse
import redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv
from src.main import create_app

load_dotenv()

listen = ['default']
#url = urlparse(os.environ.get("REDIS_TLS_URL"))
#conn = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)
url = urlparse(os.getenv("REDIS_TLS_URL"))
print(url)
conn = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)
q = Queue(connection=conn)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()