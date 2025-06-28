import socket
import asyncio
import config
import time

class UDPProtocol(asyncio.DatagramProtocol):
    """Clasa care extinde asyncio.DatagramProtocol pentru a crea o conexiune UDP asincrona"""
    def __init__(self, on_receive_callback=None):
        # callback optional ce va fi apelat la recepția unui mesaj
        self.on_receive_callback = on_receive_callback
        # obiectul folosit pentru a trimite date prin UDP
        self.transport = None  

    def connection_made(self, transport):
        """Metoda apelata automat cand conexiunea UDP este stabilita"""
        self.transport = transport

    def datagram_received(self, data, addr):
        """ Metoda apelata automat cand se primeste un pachet de date"""
        # Decodeaza datele primite în format text
        message = data.decode('utf-8')  
        
        # apeleaza functia de callback furnizata, transmitand mesajul si adresa sursa
        if self.on_receive_callback:
            self.on_receive_callback(message, addr)

    def error_received(self, exc):
        """apelata cand apare o eroare pe conexiunea UDP"""
        print(f"UDP error received: {exc}")

    def connection_lost(self, exc):
        """apelata cand conexiunea este închisă"""
        print("UDP connection closed")


class NetworkManager:
    """Clasa folosita pentru transmiterea si receptionarea datelor"""
    def __init__(self, on_receive_callback=None):
        """Initializeaza clasa si valorile variabilelor"""
        self.server_address = (config.DRONE_IP, config.DRONE_PORT)
        self.local_port = config.DRONE_PORT
        self.transport = None
        self.protocol = None
        self.on_receive_callback = on_receive_callback

        self.print_local_ip()

    def print_local_ip(self):
        """Afiseaza IP-ul local in consola"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            print(f"Local IP: {local_ip}")
        except Exception as e:
            print(f"Error getting local IP: {e}")
        finally:
            sock.close()

    async def start_receiving(self):
        """Initializeaza ascultatorul UDP in mod asincron"""
        loop = asyncio.get_running_loop()
        self.transport, self.protocol = await loop.create_datagram_endpoint(
            lambda: UDPProtocol(on_receive_callback=self.on_receive_callback),
            local_addr=('0.0.0.0', self.local_port)
        )

    def send_data(self, data: str):
        """Trimite date prin UDP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data.encode('utf-8'), self.server_address)
            sock.close()
            print("kbd")
        except Exception as e:
            print(f"Error sending data: {e}")
        
        time.sleep(config.MSG_DELAY_S)
