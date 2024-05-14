import requests
import configparser


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

    print(post_response.json())
    # if post_response.json()["livestreamUrl"] == "" and post_response.json()["StreamId"] == "":
    #     print("No livestream channel created")

    return AppData(
        apiKeyId,
        apiKeyValue,
        post_response.json()["id"],
        post_response.json()["userId"],
        post_response.json()["livestreamUrl"]
    )
