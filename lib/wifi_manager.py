import machine
import network
import socket
import re
import time
import helpers.import_helper as ih

class WifiManager:

    def __init__(self, ssid = 'WifiManager', password = 'wifimanager', reboot = True, debug = True):
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.wlan_sta.active(True)
        self.wlan_ap = network.WLAN(network.AP_IF)
        self.oled = ih.import_app().get_object("oled")
        if ih.validate_network_credentials(ssid, password) is False:
            raise Exception("Invalid network credentials")
        self.ap_ssid = ssid
        self.ap_password = password
        self.ap_authmode = 3
        self.wifi_credentials = 'wifi.dat'
        self.wlan_sta.disconnect()
        self.reboot = reboot      
        self.debug = debug

    def connect(self):
        if self.wlan_sta.isconnected():
            return
        profiles = self.read_credentials()
        for ssid, *_ in self.wlan_sta.scan():
            ssid = ssid.decode("utf-8")
            if ssid in profiles:
                password = profiles[ssid]
                if self.wifi_connect(ssid, password):
                    return
        if self.debug:
            self.oled.print_to_screen('Failed to\nconnect to WiFi')
            time.sleep(3)
    
    def disconnect(self):
        if self.wlan_sta.isconnected():
            self.wlan_sta.disconnect()

    def is_connected(self):
        return self.wlan_sta.isconnected()

    def get_address(self):
        return self.wlan_sta.ifconfig()

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
            if self.debug:
                print(error)
            pass
        profiles = {}
        for line in lines:
            ssid, password = line.strip().split(';')
            profiles[ssid] = password
        return profiles


    def wifi_connect(self, ssid, password):
        connection_message = 'Connecting to: ' + ssid
        self.oled.print_to_screen(connection_message)
        time.sleep(3)
        self.wlan_sta.connect(ssid, password)
        for attempt in range(100):
            if self.wlan_sta.isconnected():
                self.oled.print_to_screen('\nConnected!\nNetwork information:\n'+str(self.wlan_sta.ifconfig()))
                time.sleep(3)
                return True
            else:
                if attempt % 10 == 0:  # Update the display every 10 attempts to conserve resources
                    loading_dots = '.' * (attempt // 10 % 4 + 1)  # Cycle through 1-4 dots
                    self.oled.print_to_screen(connection_message + '\n' + loading_dots)
                print('.', end='')
                time.sleep_ms(100)
        self.oled.print_to_screen('\nConnect failed!')
        time.sleep(3)
        self.wlan_sta.disconnect()
        return False

    def shutdown_portal(self):
        self.wlan_ap.active(False)
        self.server_socket.close()

    def setup_web_server(self):
        self.wlan_ap.active(True)
        self.wlan_ap.config(essid = self.ap_ssid, password = self.ap_password, authmode = self.ap_authmode)
        self.server_socket = socket.socket()
        self.server_socket.close()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', 80))
        self.server_socket.listen(1)
        self.server_socket.setblocking(False)

    def run_web_server(self):
        if self.wlan_sta.isconnected():
            self.wlan_ap.active(False)
            if self.reboot:
                self.oled.print_to_screen('Device reboot\nin 5 seconds.')
                time.sleep(5)
                self.oled.clear_screen()
                machine.reset()
        try:
            self.client, addr = self.server_socket.accept()
            # If we reach here, a client has connected successfully
            # Proceed with handling the client
        except Exception as error:
            # If an exception occurs, it's likely because no client is connecting
            # Log the error if debug is enabled, but don't raise it further
            if self.debug:
                print("No client connection available:", error)
            return  # Simply return to allow for other operations, like checking for button presses

        try:
            self.client.settimeout(5.0)
            self.request = b''
            try:
                while True:
                    if '\r\n\r\n' in self.request:
                        # Fix for Safari browser
                        self.request += self.client.recv(512)
                        break
                    self.request += self.client.recv(128)
            except Exception as error:
                # It's normal to receive timeout errors in this stage, we can safely ignore them.
                if self.debug:
                    print(error)
                pass
            if self.request:
                if self.debug:
                    print(self.url_decode(self.request))
                url = re.search('(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP', self.request).group(1).decode('utf-8').rstrip('/')
                if url == '':
                    self.handle_root()
                elif url == 'configure':
                    self.handle_configure()
                else:
                    self.handle_not_found()
        except Exception as error:
            if self.debug:
                print(error)
            return
        finally:
            self.client.close()
    

    def send_header(self, status_code = 200):
        self.client.send("""HTTP/1.1 {0} OK\r\n""".format(status_code))
        self.client.send("""Content-Type: text/html\r\n""")
        self.client.send("""Connection: close\r\n""")


    def send_response(self, payload, status_code = 200):
        self.send_header(status_code)
        self.client.sendall("""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>WiFi Manager</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="icon" href="data:,">
                </head>
                <body>
                    {0}
                </body>
            </html>
        """.format(payload))
        self.client.close()


    def handle_root(self):
        self.send_header()
        self.client.sendall("""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>WiFi Manager</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="icon" href="data:,">
                </head>
                <body>
                    <h1>WiFi Manager</h1>
                    <form action="/configure" method="post" accept-charset="utf-8">
        """.format(self.ap_ssid))
        for ssid, *_ in self.wlan_sta.scan():
            ssid = ssid.decode("utf-8")
            self.client.sendall("""
                        <p><input type="radio" name="ssid" value="{0}" id="{0}"><label for="{0}">&nbsp;{0}</label></p>
            """.format(ssid))
        self.client.sendall("""
                        <p><label for="password">Password:&nbsp;</label><input type="password" id="password" name="password"></p>
                        <p><input type="submit" value="Connect"></p>
                    </form>
                </body>
            </html>
        """)
        self.client.close()


    def handle_configure(self):
        match = re.search('ssid=([^&]*)&password=(.*)', self.url_decode(self.request))
        if match:
            ssid = match.group(1).decode('utf-8')
            password = match.group(2).decode('utf-8')
            if len(ssid) == 0:
                self.send_response("""
                    <p>SSID must be providaded!</p>
                    <p>Go back and try again!</p>
                """, 400)
            elif self.wifi_connect(ssid, password):
                self.send_response("""
                    <p>Successfully connected to</p>
                    <h1>{0}</h1>
                    <p>IP address: {1}</p>
                """.format(ssid, self.wlan_sta.ifconfig()[0]))
                profiles = self.read_credentials()
                profiles[ssid] = password
                self.write_credentials(profiles)
                time.sleep(5)
            else:
                self.send_response("""
                    <p>Could not connect to</p>
                    <h1>{0}</h1>
                    <p>Go back and try again!</p>
                """.format(ssid))
                time.sleep(5)
        else:
            self.send_response("""
                <p>Parameters not found!</p>
            """, 400)
            time.sleep(5)


    def handle_not_found(self):
        self.send_response("""
            <p>Page not found!</p>
        """, 404)


    def url_decode(self, url_string):
        if not url_string:
            return b''

        if isinstance(url_string, str):
            url_string = url_string.encode('utf-8')

        bits = url_string.split(b'%')

        if len(bits) == 1:
            return url_string

        res = [bits[0]]
        appnd = res.append
        hextobyte_cache = {}

        for item in bits[1:]:
            try:
                code = item[:2]
                char = hextobyte_cache.get(code)
                if char is None:
                    char = hextobyte_cache[code] = bytes([int(code, 16)])
                appnd(char)
                appnd(item[2:])
            except Exception as error:
                if self.debug:
                    print(error)
                appnd(b'%')
                appnd(item)

        return b''.join(res)

