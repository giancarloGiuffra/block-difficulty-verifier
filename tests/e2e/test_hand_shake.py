import unittest
import time

from bdv import client
from tests import helpers


class TestHandShake(unittest.TestCase):

    def test_hand_shake_begins_with_version_message(self):
        ip_to_connect = '127.0.0.1'

        fake_client = helpers.FakeClient(ip_to_connect)
        fake_client.start()

        time.sleep(0.001)

        bdv_client = client.Client(ip_to_connect, fake_client.port_number())
        bdv_client.start()

        time.sleep(0.001)

        fake_client.stop()
        bdv_client.join()
        fake_client.join()

        self.assertEqual(b'version', fake_client.messages_received[0])
