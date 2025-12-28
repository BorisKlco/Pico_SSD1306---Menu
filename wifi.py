import time

class Wifi:
    def __init__(self, uart):
        self.uart = uart
        self.connected_ip = None
        self.send("AT+RST", 2)
        self.send("AT+CWMODE=1")

    def connect(self, ssid, password):
        self.send(f'AT+CWJAP="{ssid}","{password}"', 8)
        ip_info = self.send("AT+CIFSR", 2)
        print("IP:", ip_info)
        if ip_info:
            for l in ip_info.decode().split("\r\n"):
                if l.startswith("+CIFSR:STAIP"):
                    ip = l.split('"')
                    self.connected_ip = ip[1]


    def send(self, cmd, wait=1):
        self.uart.write(cmd + '\r\n')
        time.sleep(wait)
        if self.uart.any():
            return self.uart.read()
        return b""

    def scan(self):
        resp = self.send("AT+CWLAP", 5)
        networks = []
        if resp:
            for line in resp.decode().split("\r\n"):
                if line.startswith("+CWLAP:"):
                    parts = line[line.find("(")+1:line.find(")")].split(",")
                    ssid = parts[1].strip('"')
                    if ssid:
                        networks.append(ssid)
        return networks
