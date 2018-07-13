import socket
import os
import threading
from datetime import datetime

from bdv import entities
from bdv import messages


class Client(threading.Thread):

    def __init__(self, node_ip, port):
        super().__init__()
        self.node_ip = node_ip
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.node_ip, self.port))
        message = messages.VersionMessage(70015,
                                          1,
                                          datetime.now(),
                                          entities.NetworkAddress(1, self.node_ip, self.port),
                                          entities.NetworkAddress(1, '0.0.0.0', 0),
                                          os.urandom(8),
                                          entities.VariableLengthString(b'/Satoshi:0.16.0/'),
                                          0)
        s.sendall(message.serialize())
        s.close()
