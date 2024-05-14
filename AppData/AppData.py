import requests
import configparser
import livepeer
from livepeer.models import components


class AppData:
    def __init__(self, apiKeyId, apiKeyValue, deviceID, userID, streamingChannelUrl):
        self.ApiKeyId = apiKeyId,
        self.ApiKeyValue = apiKeyValue
        self.DeviceID = deviceID
        self.UserID = userID
        self.StreamingChannelUrl = streamingChannelUrl


def get_app_data():
    # make request to get the app data
    config = configparser.ConfigParser()
    config.read("config.ini")
    uri = config["Server_Settings"]["API_URI"]

    apiKeyId = config["Device_Properties"]["API_KEY_ID"]
    apiKeyValue = config["Device_Properties"]["API_KEY_VALUE"]
    deviceId = config["Device_Properties"]["DEVICE_ID"]

    body = {
        "ApiKeyId": apiKeyId,
        "ApiKeyValue": apiKeyValue,
        "DeviceId": deviceId
    }

    url_post = uri + "/api/device/get/key"
    post_response = requests.post(url_post, json=body)
    livestreamUrl = ""

    if not post_response.json()["livestreamUrl"] and not post_response.json()["streamId"]:
        livepeerApiKey = config["Api_Keys"]["LIVEPEER_API_KEY"]
        client = livepeer.Livepeer(
            api_key = "bd39e9bb-a707-4aab-9c03-25e9a2171b83"
        )
        req = components.NewStreamPayload(
            name = deviceId + "_streaming_channel",
        )
        res = client.stream.create(req)
        if res.stream is not None:
            streamId = res.stream.playback_id
            livestreamUrl = "rtmp://rtmp.livepeer.com/live/" + res.stream.stream_key

            body = {
                "ApiKeyId": apiKeyId,
                "ApiKeyValue": apiKeyValue,
                "DeviceId": deviceId,
                "StreamId": streamId,
                "LivestreamUrl": livestreamUrl
            }

            url_post = uri + "/api/device/get/key"
            put_response = requests.put(url_post, json=body)
            print(put_response)
        else:
            return
    else:
        livestreamUrl = post_response.json()["livestreamUrl"]


    return AppData(
        apiKeyId,
        apiKeyValue,
        post_response.json()["id"],
        post_response.json()["userId"],
        livestreamUrl
    )
