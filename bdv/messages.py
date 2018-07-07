from bdv import crypto
from io import BytesIO


class NetworkMessage(object):
    MAGIC_BYTES = b'\xf9\xbe\xb4\xd9'

    def __init__(self, command, payload):
        self.command = command
        self.payload = payload

    def serialize(self):
        return self.header() + self.payload

    def header(self):
        return self.MAGIC_BYTES + self.serialized_command() + self.payload_length() + self.checksum()

    def serialized_command(self):
        return self.command.ljust(12, b'\x00')

    def payload_length(self):
        return (len(self.payload)).to_bytes(4, byteorder='little')

    def checksum(self):
        return crypto.double_sha256(self.payload)[:4]

    @classmethod
    def parse(cls, serialized_message):
        stream = BytesIO(serialized_message)
        assert stream.read(4) == cls.MAGIC_BYTES, "not valid magic bytes"
        command = stream.read(12)
        payload_length = int.from_bytes(stream.read(4), byteorder='little')
        checksum = stream.read(4)
        payload = stream.read(payload_length)
        assert checksum == crypto.double_sha256(payload)[:4], "not valid checksum"
        return cls(cls.strip_zeros(command), payload)

    @classmethod
    def strip_zeros(cls, command):
        return bytes([byte for byte in command if byte != 0])


class VersionMessage(NetworkMessage):

    def __init__(self, version, services, date_time, to_address, from_address, nonce, user_agent, last_block_received):
        self.version = version
        self.services = services
        self.date_time = date_time
        self.to_address = to_address
        self.from_address = from_address
        self.nonce = nonce
        self.user_agent = user_agent
        self.last_block_received = last_block_received
        super().__init__(b'version', self.build_payload())

    def build_payload(self):
        return self.version.to_bytes(4, byteorder='little') \
                + self.services.to_bytes(8, byteorder='little') \
                + int(self.date_time.timestamp()).to_bytes(8, byteorder='little') \
                + self.to_address.serialize() \
                + self.from_address.serialize() \
                + self.nonce \
                + self.user_agent.serialize() \
                + self.last_block_received.to_bytes(4, byteorder='little')
