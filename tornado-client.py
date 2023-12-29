# client.py
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.websocket import websocket_connect
import time
from concurrent.futures import ThreadPoolExecutor


@gen.coroutine
def client():
    conn = yield websocket_connect("ws://localhost:8888")
    yield conn.write_message("Hello, World!")
    yield conn.read_message()


def measure_latency():
    start_time = time.time()
    IOLoop.current().run_sync(client)
    end_time = time.time()
    latency = end_time - start_time
    print(f"Latency: {latency} seconds")


def measure_throughput(num_messages):
    start_time = time.time()
    for _ in range(num_messages):
        IOLoop.current().run_sync(client)
    end_time = time.time()
    throughput = num_messages / (end_time - start_time)
    print(f"Throughput: {throughput} messages per second")


def measure_scalability(num_clients):
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        start_time = time.time()
        executor.map(lambda _: IOLoop.current().run_sync(client), range(num_clients))
        end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken for {num_clients} clients: {time_taken} seconds")


measure_latency()
measure_throughput(60)
measure_scalability(10)