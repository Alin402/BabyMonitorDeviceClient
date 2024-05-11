import json
import random
import time
import asyncio
#import adafruit_dht
#import board

from MessageContents.SendTemperatureSensorDataMessageContent import SendTemperatureSensorDataMessageContent
from Messages.Messages import get_send_temperature_sensor_data_message


def is_numeric(value):
    return isinstance(value, (int, float, complex))


async def send_temperature_sensor_data(websocket, appData, event, lock):
    # try:
    #     dhtDevice = adafruit_dht.DHT11(board.D23)
    # except RuntimeError as e:
    #     print(e.args[0])
    #     exit()
    with lock:
        userID = appData.UserID

        # start sending temperature data
        print("sending temperature data...")
        while event.is_set():
            try:
                print("sending temperature...")
                # temperatureC = dhtDevice.temperature
                # if temperatureC is None:
                #     return
                temperatureC = random.uniform(20, 30);
                temperatureF = temperatureC * (9 / 5) + 32
                # humidity = dhtDevice.humidity
                humidity = random.uniform(10, 20)

                if not is_numeric(temperatureC) or temperatureC == 0:
                    await asyncio.sleep(1)
                    continue

                print(temperatureC)

                messageContent = SendTemperatureSensorDataMessageContent(userID, temperatureF, temperatureC, humidity)
                message = get_send_temperature_sensor_data_message(messageContent)
                if websocket.open:
                    await websocket.send(json.dumps(message))
                await asyncio.sleep(1)
            except Exception as e:
                print(e.args[0])
                await asyncio.sleep(1)
                continue
