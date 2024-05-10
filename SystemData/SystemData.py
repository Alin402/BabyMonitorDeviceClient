import random
import time
import json
import asyncio
from MessageContents.SendSystemDataContent import SendSystemDataContent
from Messages.Messages import get_send_system_data_message


async def send_system_data(websocket, appData, event, lock):
    userID = appData.UserID
    with lock:
        while event.is_set():
            try:
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
                    if file is None:
                        await asyncio.sleep(2)
                        continue
                    temperature_str = file.readline()
                    temperature = float(temperature_str) / 1000.0
                    print("sending system temperature..." + str(temperature))
                    messageContent = SendSystemDataContent(userID, temperature)
                    message = get_send_system_data_message(messageContent)
                    if websocket.open:
                        await websocket.send(json.dumps(message))
                    await asyncio.sleep(2)
            except Exception as e:
                print("Failed to send system data:", e)
                await asyncio.sleep(2)
                continue
