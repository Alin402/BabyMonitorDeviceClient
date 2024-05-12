import wifi
from wifi import Cell, Scheme


def connect_to_wifi(ssid, password):
    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        if cell.ssid == ssid:
            scheme = Scheme.for_cell('wlan0', ssid, cell, password)
            scheme.save()
            scheme.activate()
            print("Connected to Wi-Fi network:", ssid)
            return
