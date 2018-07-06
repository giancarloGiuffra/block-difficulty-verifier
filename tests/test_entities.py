import unittest
from binascii import unhexlify
from bdv import entities


class TestEntities(unittest.TestCase):

    def test_serialize_network_addresses(self):
        address = entities.NetworkAddress(1, '10.0.0.1', 8333)
        self.assertEqual(unhexlify('010000000000000000000000000000000000ffff0a000001208d'), address.serialize())

    def test_serialize_variable_length_string(self):
        pass

    def test_serialize_variable_length_integer(self):
        self.assertEqual(b'\xfc', self.serialized_integer(b'\xfc'))
        self.assertEqual(b'\xfd\xff\xff', self.serialized_integer(b'\xff\xff'))
        self.assertEqual(b'\xfe\xff\xff\xff\xff', self.serialized_integer(b'\xff\xff\xff\xff'))
        self.assertEqual(b'\xff\xff\xff\xff\xff\xee\x00\x00\x00', self.serialized_integer(b'\xff\xff\xff\xff\xee'))

    def test_serialize_variable_length_string(self):
        message = b'satoshi'
        expected = b'\x07' + message
        self.assertEqual(expected, entities.VariableLengthString(message).serialize())

    @staticmethod
    def serialized_integer(one_byte_integer):
        return entities.VariableLengthInteger(TestEntities.little_endian(one_byte_integer)).serialize()

    @staticmethod
    def little_endian(integer_in_bytes):
        return int.from_bytes(integer_in_bytes, byteorder='little')
