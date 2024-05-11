import time
import asyncio


async def receive_messages(websocket, appData, event, lock):
    with lock:
        print("receiving messages...")
        while event.is_set():
            message = await websocket.recv()
            print("Received message: ", message["MessageType"])
            await asyncio.sleep(2)
