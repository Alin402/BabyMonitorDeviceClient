import os
import subprocess


def configure_and_connect_wifi(ssid, password):
    config_lines = [
        'country=US',
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        '\n',
        'network={',
        '\tssid="{}"'.format(ssid),
        '\tpsk="{}"'.format(password),
        '}'
    ]
    config = '\n'.join(config_lines)

    try:
        # Write the configuration to a temporary file
        with open("/etc/wpa_supplicant/wpa_temp.conf", "w") as wifi:
            wifi.write(config)

        # Move the temporary file to the correct location
        subprocess.run(["sudo", "mv", "/etc/wpa_supplicant/wpa_temp.conf", "/etc/wpa_supplicant/wpa_supplicant.conf"])

        # Restart the wpa_supplicant service to apply the changes
        subprocess.run(["sudo", "systemctl", "restart", "wpa_supplicant"])

        print("Wi-Fi configuration added. Connected to Wi-Fi network:", ssid)
    except Exception as e:
        print("Error:", e)
