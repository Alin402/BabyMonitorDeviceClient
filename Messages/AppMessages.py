import json


async def receive_messages(websocket, appData, event, lock, restart_callback):
    with lock:
        print("receiving messages...")
        while event.is_set():
            print("enter messages data loop...")
            try:
                message = await websocket.recv()
                jsonMessage = json.loads(message)
                messageType = jsonMessage["MessageType"]
                if messageType == 8:
                    restart_callback(websocket)  # Call the restart callback function
            except Exception as e:
                print(e)
                continue
