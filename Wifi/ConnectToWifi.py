import wifi
from wifi import Cell, Scheme


def connect_to_wifi(ssid, password):
    # Scan for available Wi-Fi networks
    cells = wifi.Cell.all('wlan0')

    # Check if the specified Wi-Fi network is found
    for cell in cells:
        if cell.ssid == ssid:
            print(cell.ssid)
            # Connect to the specified Wi-Fi network
            scheme = Scheme.for_cell('wlan0', ssid, cell, password)
            scheme.save()
            scheme.activate()
            print("Connected to Wi-Fi network:", ssid)
            return

    print("Wi-Fi network not found:", ssid)
