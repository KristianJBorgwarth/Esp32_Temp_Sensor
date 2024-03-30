import machine
import network
import socket
import re
import time
import helpers.import_helper as ih
from lib.wifi.wifi_credentials_handler import WifiCredentialsHandler
from lib.wifi.web_page_handler import WebPageHandler
import lib.wifi.url_decoder as url_decoder
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
        self.cd_handler = WifiCredentialsHandler()
        
    def connect(self):
        if self.wlan_sta.isconnected():
            return
        profiles = self.cd_handler.read_credentials()
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
            wp_handler = WebPageHandler(self.client)
        except Exception as error:
            if self.debug:
                print("No client connection available:", error)
            return
        try:
            self.client.settimeout(5.0)
            self.request = b''
            try:
                while True:
                    if '\r\n\r\n' in self.request:
                        self.request += self.client.recv(512)
                        break
                    self.request += self.client.recv(128)
            except Exception as error:
                if self.debug:
                    print(error)
                pass
            if self.request:
                if self.debug:
                        print(url_decoder.url_decode(self.request))
                url = re.search('(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP', self.request).group(1).decode('utf-8').rstrip('/')
                if url == '':
                    wp_handler.handle_root(self.wlan_sta, self.ap_ssid)
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

    def handle_configure(self):
        match = re.search('ssid=([^&]*)&password=(.*)', url_decoder.url_decode(self.request))
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
                profiles = self.cd_handler.read_credentials()
                profiles[ssid] = password
                self.cd_handler.write_credentials(profiles)
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
