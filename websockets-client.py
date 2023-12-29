# client.py
import asyncio
import websockets
import time
from concurrent.futures import ThreadPoolExecutor

async def client():
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send('Hello World!')
        await websocket.recv()

def measure_latency():
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(client())
    end_time = time.time()
    latency = end_time - start_time
    print(f"Latency: {latency} seconds")

def measure_throughput(num_messages):
    start_time = time.time()
    for _ in range(num_messages):
        asyncio.get_event_loop().run_until_complete(client())
    end_time = time.time()
    throughput = num_messages / (end_time - start_time)
    print(f"Throughput: {throughput} messages per second")

def measure_scalability(num_clients):
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        start_time = time.time()
        executor.map(lambda _: asyncio.get_event_loop().run_until_complete(client()), range(num_clients))
        end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken for {num_clients} clients: {time_taken} seconds")

measure_latency()
measure_throughput(60)
measure_scalability(10)
