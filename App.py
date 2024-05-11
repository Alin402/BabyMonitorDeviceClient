import json
import time
import configparser
import threading
import copy
import asyncio

import websockets

from MessageContents.ConnectToServerMessageContent import ConnectToServerMessageContent
from Messages.Messages import get_connect_to_server_message
from AppData.AppData import get_app_data
from Sensors.TemperatureSensor import send_temperature_sensor_data
from Messages.AppMessages import receive_messages
from Livestream.StartLivestream import start_live_stream
from SystemData.SystemData import send_system_data


async def connect_to_server():
    config = configparser.ConfigParser()
    config.read("config.ini")
    uri = config["Server_Settings"]["SERVER_URI"]

    appData = get_app_data()
    print(appData.UserID, appData.DeviceID)

    send_temp_data_event = threading.Event()
    temp_data_websocket_lock = threading.Lock()

    receive_messages_websocket_lock = threading.Lock()
    receive_messages_event = threading.Event()

    send_system_data_websocket_lock = threading.Lock()
    send_system_data_event = threading.Event()

    send_livestream_data_event = threading.Event()

    async def restart_callback():
        # Place your restart logic here
        # For example, you can call connect_to_server() again
        print("Restarting...")
        await connect_to_server()

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                messageContent = ConnectToServerMessageContent(appData.ApiKeyId[0], appData.ApiKeyValue, appData.DeviceID, appData.UserID, appData.StreamingChannelUrl)
                message = get_connect_to_server_message(messageContent)
                await websocket.send(json.dumps(message))
                print("Connected to server...")

                send_temp_data_event.set()
                receive_messages_event.set()
                send_system_data_event.set()
                send_livestream_data_event.set()

                livestream_coroutine = asyncio.create_task(start_live_stream(send_livestream_data_event))
                system_data_coroutine = asyncio.create_task(send_system_data(websocket, copy.deepcopy(appData), send_system_data_event, send_system_data_websocket_lock))
                await send_temperature_sensor_data(websocket, copy.deepcopy(appData), send_temp_data_event,
                                             temp_data_websocket_lock)
                await receive_messages(websocket, copy.deepcopy(appData), receive_messages_event,
                                 receive_messages_websocket_lock, restart_callback)
                await start_live_stream(send_livestream_data_event)
                await send_system_data(websocket, copy.deepcopy(appData), send_system_data_event, send_system_data_websocket_lock)

                # await asyncio.gather(
                #     send_temperature_sensor_data(websocket, copy.deepcopy(appData), send_temp_data_event,
                #                                  temp_data_websocket_lock),
                #     receive_messages(websocket, copy.deepcopy(appData), receive_messages_event,
                #                      receive_messages_websocket_lock, restart_callback),
                #     livestream_coroutine,
                #     system_data_coroutine
                # )
        except Exception as e:
            print(e)
            continue
        finally:
            print("Closing connection...")
            send_temp_data_event.clear()
            receive_messages_event.clear()
            send_system_data_event.clear()
            send_livestream_data_event.clear()


asyncio.run(connect_to_server())
