class NetworkAddress(object):

    def __init__(self, services, ip_address, port, time = None):
        self.services = services
        self.ip_address = ip_address
        self.port = port
        self.time = time

    def serialize(self):
        return self.serialized_time() \
                + self.services.to_bytes(8, byteorder='little') \
                + self.serialized_ip_address() \
                + self.port.to_bytes(2, byteorder='big')

    def serialized_ip_address(self):
        return b'\x00'*10 \
                + b'\xff'*2 \
                + b''.join([int(octet).to_bytes(1, byteorder='big') for octet in self.ip_address.split('.')])

    def serialized_time(self):
        return b'' if self.time is None else self.time.to_bytes(4, byteorder='little')


class VariableLengthInteger(object):

    def __init__(self, integer):
        self.integer = integer

    def serialize(self):
        if self.integer < VariableLengthInteger.to_integer(b'\xfd'):
            return self.integer.to_bytes(1, byteorder='little')
        elif self.integer <= VariableLengthInteger.to_integer(b'\xff\xff'):
            return b'\xfd' + self.integer.to_bytes(2, byteorder='little')
        elif self.integer <= VariableLengthInteger.to_integer(b'\xff\xff\xff\xff'):
            return b'\xfe' + self.integer.to_bytes(4, byteorder='little')
        else:
            return b'\xff' + self.integer.to_bytes(8, byteorder='little')

    @staticmethod
    def to_integer(integer_in_bytes):
        return int.from_bytes(integer_in_bytes, byteorder='little')


class VariableLengthString(object):

    def __init__(self, string):
        self.string = string

    def serialize(self):
        return VariableLengthInteger(len(self.string)).serialize() + self.string
