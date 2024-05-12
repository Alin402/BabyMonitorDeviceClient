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

        # give access and writing. may have to do this manually beforehand
        os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

        # writing to file
        with open("sudo /etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
            wifi.write(config)

        print("Wifi config added. Refreshing configs")
        os.popen("sudo wpa_cli -i wlan0 reconfigure")
    except Exception as e:
        print("Exception in connect to wifi " + str(e))
