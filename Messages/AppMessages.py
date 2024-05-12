import asyncio
import json
from LifetimeOperations.RestartDevice import restart_device


async def receive_messages(websocket, appData, event, lock):
    with lock:
        print("receiving messages...")
        while event.is_set():
            print("enter messages data loop...")
            try:
                message = await websocket.recv()
                jsonMessage = json.loads(message)
                messageType = jsonMessage["MessageType"]
                if messageType == 8:
                    task = asyncio.create_task(restart_device())
                    await asyncio.gather(task)
            except Exception as e:
                print("Exception in app messages: " + str(e))
                continue
