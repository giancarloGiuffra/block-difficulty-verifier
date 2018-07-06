import unittest
from binascii import unhexlify
from bdv import messages
from bdv import entities
from datetime import datetime


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

    @unittest.skip
    def test_serialize_version_message(self):
        version = 70015 #4 bytes
        services = 1024 #8 bytes
        timestamp = datetime(2018, 7, 6) #to unix timestamp to 8 bytes
        to_address = entities.NetworkAddress(services, '10.0.0.1', 8333)
        from_address = entities.NetworkAddress(services, '10.0.0.1', 8333)
        # random nonce 8 bytes
        user_agent = entities.VariableLengthString(b'/Satoshi:0.7.2/')
        last_block_received = 0 # 4 bytes
        messages.VersionMessage(version, services, timestamp, to_address, from_address, user_agent, last_block_received)
