import threading
import socket
from bdv import messages


class FakeClient(threading.Thread):

    def __init__(self, host, port=0):
        super().__init__()
        self.host = host
        self.port = port
        self.messages_received = []
        self.server = None
        self.stop_signal = b'stop'

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            self.server = server
            server.bind((self.host, self.port))
            server.listen(5)
            while True:
                connection, address = server.accept()
                with connection:
                    message_received = connection.recv(1024)
                    parsed_message = messages.NetworkMessage.parse(message_received)
                    self.messages_received.append(parsed_message.command)
                    if parsed_message.command == self.stop_signal:
                        server.close()
                        break

    def stop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.host, self.port_number()))
            stop_message = messages.NetworkMessage(self.stop_signal, b'')
            client.sendall(stop_message.serialize())

    def port_number(self):
        return self.server.getsockname()[1]
