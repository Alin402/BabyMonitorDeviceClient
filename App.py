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

send_temp_data_event = threading.Event()
temp_data_websocket_lock = threading.Lock()

receive_messages_websocket_lock = threading.Lock()
receive_messages_event = threading.Event()

send_system_data_websocket_lock = threading.Lock()
send_system_data_event = threading.Event()

send_livestream_data_event = threading.Event()

async def close_websocket(websocket):
    if websocket.open:
        await websocket.close()
        print("Websocket connection closed")

async def restart_callback(websocket):
    print("Restarting...")
    close_websocket_task = asyncio.create_task(close_websocket(websocket))
    connect_server_task = asyncio.create_task(connect_to_server())
    await asyncio.gather(close_websocket_task, connect_server_task)


async def connect_to_server():
    config = configparser.ConfigParser()
    config.read("config.ini")
    uri = config["Server_Settings"]["SERVER_URI"]

    appData = get_app_data()
    print(appData.UserID, appData.DeviceID)

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                messageContent = ConnectToServerMessageContent(appData.ApiKeyId[0], appData.ApiKeyValue,
                                                               appData.DeviceID, appData.UserID,
                                                               appData.StreamingChannelUrl)
                message = get_connect_to_server_message(messageContent)
                await websocket.send(json.dumps(message))
                print("Connected to server...")

                send_temp_data_event.set()
                receive_messages_event.set()
                send_system_data_event.set()
                send_livestream_data_event.set()

                send_temp_task = asyncio.create_task(
                    send_temperature_sensor_data(websocket, copy.deepcopy(appData), send_temp_data_event,
                                                 temp_data_websocket_lock))
                receive_msgs_task = asyncio.create_task(
                    receive_messages(websocket, copy.deepcopy(appData), receive_messages_event,
                                     receive_messages_websocket_lock, restart_callback))
                livestream_coroutine = asyncio.create_task(start_live_stream(send_livestream_data_event))
                system_data_coroutine = asyncio.create_task(
                    send_system_data(websocket, copy.deepcopy(appData), send_system_data_event,
                                     send_system_data_websocket_lock))

                await asyncio.gather(
                    send_temp_task,
                    receive_msgs_task,
                    livestream_coroutine,
                    system_data_coroutine
                )
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
