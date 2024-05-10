import time
import asyncio


async def receive_messages(websocket, appData, event, lock):
    with lock:
        while event.is_set():
            print("receiving messages...")
            await asyncio.sleep(2)