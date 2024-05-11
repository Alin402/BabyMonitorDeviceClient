import json


async def receive_messages(websocket, appData, event, lock, restart_callback, task1, task2, task3, task4):
    with lock:
        print("receiving messages...")
        while event.is_set():
            try:
                message = await websocket.recv()
                jsonMessage = json.loads(message)
                messageType = jsonMessage["MessageType"]
                if messageType == 8:
                    await restart_callback(task1, task2, task3, task4)  # Call the restart callback function
            except Exception as e:
                print(e)
                continue
