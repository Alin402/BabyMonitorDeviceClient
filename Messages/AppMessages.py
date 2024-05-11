import time
import asyncio
import json


async def receive_messages(websocket, appData, event, lock):
    with lock:
        print("receiving messages...")
        while event.is_set():
            try:
                message = await websocket.recv()
                jsonMessage = json.loads(message)
                messageType = jsonMessage["MessageType"]
                if messageType is 8:
                    print("Restarting...")

                await asyncio.sleep(2)
            except Exception as e:
                print(e)
                continue
