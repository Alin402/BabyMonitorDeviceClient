import time
import asyncio


async def receive_messages(websocket, appData, event, lock):
    with lock:
        print("receiving messages...")
        while event.is_set():
            try:
                message = await websocket.recv()
                print("Received message: ", message.json()["MessageType"])
                await asyncio.sleep(2)
            except Exception as e:
                print(e)
                continue
