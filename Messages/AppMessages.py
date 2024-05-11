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
                    await restart_callback(websocket)
            except Exception as e:
                print("Exception in app messages: " + str(e))
                continue
