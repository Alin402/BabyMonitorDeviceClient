import os


def connect_to_wifi(ssid, password):
    try:
        config_lines = [
            'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
            'update_config=1',
            'country=US',
            '\n',
            'network={',
            '\tssid="{}"'.format(ssid),
            '\tpsk="{}"'.format(password),
            '}'
        ]
        config = '\n'.join(config_lines)

        # Give access and writing permissions. May have to do this manually beforehand.
        os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

        # Write to the configuration file.
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
            wifi.write(config)

        print("Wi-Fi configuration added. Refreshing Wi-Fi configurations...")
        # Refresh Wi-Fi configurations.
        os.popen("sudo wpa_cli -i wlan0 reconfigure")

        # Connect to the configured Wi-Fi network.
        print("Connecting to Wi-Fi network:", ssid)
        os.popen("sudo wpa_cli -i wlan0 reassociate")
    except Exception as e:
        print("Exception in connect to wifi " + str(e))
