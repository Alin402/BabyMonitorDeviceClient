import time
import pywifi
from pywifi import const


def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assuming only one wireless interface exists

    iface.disconnect()  # Disconnect from any currently connected network

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()  # Remove existing profiles
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(5)  # Wait for connection to establish

    if iface.status() == const.IFACE_CONNECTED:
        print("Connected to Wi-Fi network:", ssid)
    else:
        print("Failed to connect to Wi-Fi network")
