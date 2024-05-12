import subprocess


def connect_to_wifi(ssid, password):
    try:
        # Execute the iwlist command to scan for available networks
        result = subprocess.run(['iwlist', 'wlan0', 'scan'], capture_output=True, text=True)

        # Parse the output to extract SSIDs
        networks = []
        current_ssid = None
        for line in result.stdout.split('\n'):
            if 'ESSID:' in line:
                current_ssid = line.split('"')[1]
            elif 'Quality=' in line and current_ssid:
                networks.append((current_ssid, line.split('Quality=')[1].split()[0]))
                current_ssid = None

        for network in networks:
            print("SSID:", network[0], "Signal:", network[1])
    except Exception as e:
        print("Error:", e)
        return []
