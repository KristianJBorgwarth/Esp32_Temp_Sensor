class WifiCredentialsHandler:
    def __init__(self):
        self.wifi_credentials = "wifi.dat"
    
    def write_credentials(self, profiles):
        lines = []
        for ssid, password in profiles.items():
            lines.append('{0};{1}\n'.format(ssid, password))
        with open(self.wifi_credentials, 'w') as file:
            file.write(''.join(lines))

    def read_credentials(self):
        lines = []
        try:
            with open(self.wifi_credentials) as file:
                lines = file.readlines()
        except Exception as error:
                print(error)
        profiles = {}
        for line in lines:
            ssid, password = line.strip().split(';')
            profiles[ssid] = password
        return profiles