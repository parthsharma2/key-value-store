import argparse
import sys
import logging
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

class Client:

    def __init__(self, host='127.0.0.1', port=25552):
        """
        Creates a client to connect to the KeyValueStore REST Server.

        :param host: The host address to connect to, defaults to 127.0.0.1
        :type host: str, optional
        :param port: The port the server is running on, defaults to 25552
        :type host: int, optional
        :param size: The buffer size of data to receive
        :type size: int, optional
        """
        self.host = host
        self.port = port
        self.url = f'http://{host}:{port}/api'

        # Check if the REST server is running
        try:
            requests.get(f'{self.url}/ping')
        except requests.exceptions.ConnectionError:
            print(f"Couldn't connect to {self.host}:{self.port}!",
                  "Make sure the KeyValueStore REST server is running.")
            self.exit(1)
        except Exception as e:
            logger.exception(e)
            self.exit(1)

    def execute(self, cmd, *args):
        """Execute a command"""
        if cmd.lower() == 'get':
            response = requests.get(f'{self.url}/{args[0]}')

            if 'result' in response.json():
                return response.json()['result']

        elif cmd.lower() == 'set':
            response = requests.post(f'{self.url}/{args[0]}',
                                     json={'value': args[1]})

            if 'result' in response.json():
                return response.json()['result']

        elif cmd.lower() == 'delete':
            response = requests.delete(f'{self.url}/{args[0]}')

            if 'result' in response.json():
                return response.json()['result']

        elif cmd.lower() == 'exit':
            self.exit(0)

        else:
            return 'Unrecognized command!'

    def io_loop(self):
        """Begins the IO loop allowing you to send/receive data to and from the server."""
        while True:
            try:
                inp = input('> ')

                cmd, *args = inp.strip().split()
                response = self.execute(cmd, *args)

                print(response)

            except (KeyboardInterrupt, EOFError):
                self.exit(0)
            except Exception as e:
                logger.exception(e)
                print('An unexpected error occured!')

    def exit(self, exit_code):
        """Exit client"""
        sys.exit(exit_code)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1', type=str,
                        help='hostname/IP to run the server on. Default: 127.0.0.1')
    parser.add_argument('-p', '--port', default=25552, type=int,
                        help='port to run the server on. Default: 25552')

    args = parser.parse_args()

    client = Client(args.host, args.port)
    client.io_loop()

if __name__ == "__main__":
    main()