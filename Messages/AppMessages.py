import json


async def receive_messages(websocket, appData, event, lock, restart_callback):
    with lock:
        print("receiving messages...")
        while event.is_set():
            try:
                message = await websocket.recv()
                jsonMessage = json.loads(message)
                messageType = jsonMessage["MessageType"]
                if messageType == 8:
                    restart_callback()  # Call the restart callback function
            except Exception as e:
                print(e)
                continue
