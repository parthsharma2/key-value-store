import unittest
import subprocess
import time

from kvs.client import Client


class TestClient(unittest.TestCase):

    def setUp(self):
        self.p = subprocess.Popen(['python', '-m', 'kvs.server'],
                                  stdout=subprocess.PIPE)
        # Wait for a second for the server to start
        time.sleep(1)

    def test_client_connection(self):
        assert Client()

    def test_client_executes_all_commands_successfully(self):
        client = Client()
        assert client.execute('get', 'a') == 'null'
        assert client.execute('set', 'a', '2') == 'a:2 stored successfully'
        assert client.execute('get', 'a') == '2'
        assert client.execute('delete', 'a') == 'a deleted'
        assert client.execute('delete', 'a') == 'a does not exist'
        assert client.execute('get', 'a') == 'null'
        assert client.execute('some_command', 'some_arg') == 'Unrecognized command!'

    def tearDown(self):
        self.p.kill()