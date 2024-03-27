import machine 
import network
import socket
import re 
import time 

class WifiManager:
    def __init__(self, ssid = "wifimanager", 
                 password = "wifimanager", 
                 reboot = True, 
                 debug = False):
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.wlan_sta.active(True)
        self.wlan_ap = network.WLAN(network.AP_IF)

        self.d_ssid = ssid
        self.d_password = password
        self.reboot = reboot
        self.debug = debug
        if self.validate_ssid_password(self.d_ssid, self.d_password) == False:
            raise ValueError("SSID or password invalid")

    
    def validate_ssid_password(self, ssid, password):
        if len(ssid) < 1 or len(ssid) > 32:
            return False
        if len(password) < 8 or len(password) > 64:
            return False
        return True

    def start_web_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(1)
        print("Web server runniing on http://{}:{}".format(addr[0], addr[1]))
        
        while True:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            conn.sendall('HTTP/1.1 200 OK\n')
            conn.sendall('Content-Type: text/html\n')
            conn.sendall('\n')
            conn.sendall('<h1>Hello, World!</h1>')
            conn.close()
        
    def generate_web_page(self):
        html = """
        <html>
        <head>
        <title>Wifi Manager</title>
        </head>
        <body>
        <h1>Wifi Manager</h1>
        <form action="/wifi" method="post">
        SSID: <input type="text" name="ssid"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>
        """
        return html
