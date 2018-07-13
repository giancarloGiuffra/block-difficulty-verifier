import unittest
from binascii import unhexlify, hexlify
from datetime import datetime

from bdv import entities
from bdv import messages


class TestMessages(unittest.TestCase):

    def test_parse_message(self):
        message = messages.NetworkMessage(b'command', b'\x01\x02\x03\x04')
        serialized_message = message.serialize()
        parsed_message = messages.NetworkMessage.parse(serialized_message)
        self.assertEqual(message.command, parsed_message.command)
        self.assertEqual(message.payload, parsed_message.payload)

    def test_parse_message_invalid_magic(self):
        self.assertRaises(AssertionError, messages.NetworkMessage.parse, b'\x01\x02\x03\x04')

    def test_parse_message_invalid_checksum(self):
        message_with_invalid_checksum = unhexlify("f9beb4d976657261636b000000000000000000005df6e0ff")
        self.assertRaises(AssertionError, messages.NetworkMessage.parse, message_with_invalid_checksum)

    def test_parse_message_zero_payload(self):
        message = unhexlify("f9beb4d976657261636b000000000000000000005df6e0e2")
        parsed_message = messages.NetworkMessage.parse(message)
        self.assertEqual(b'verack', parsed_message.command)
        self.assertEqual(b'', parsed_message.payload)

    def test_serialize_verack(self):
        verack = messages.NetworkMessage(b'verack', b'')
        self.assertEqual(unhexlify("f9beb4d976657261636b000000000000000000005df6e0e2"), verack.serialize())

    def test_serialize_version_message(self):
        version = 60002
        services = 1
        timestamp = datetime(2012, 12, 18, 19, 12, 33)
        to_address = entities.NetworkAddress(services, '0.0.0.0', 0)
        from_address = entities.NetworkAddress(services, '0.0.0.0', 0)
        nonce = b'\x3B\x2E\xB3\x5D\x8C\xE6\x17\x65'
        user_agent = entities.VariableLengthString(b'/Satoshi:0.7.2/')
        last_block_received = 212672
        message = messages.VersionMessage(version, services, timestamp, to_address, from_address, nonce, user_agent,
                                          last_block_received)
        expected = "f9beb4d976657273696f6e0000000000" \
                   "640000003B648D5A62ea000001000000" \
                   "0000000011b2d0500000000001000000" \
                   "0000000000000000000000000000ffff" \
                   "00000000000001000000000000000000" \
                   "0000000000000000ffff000000000000" \
                   "3b2eb35d8ce617650f2f5361746f7368" \
                   "693a302e372e322fc03e0300"
        self.assertEqual(unhexlify(expected), message.serialize())
