import argparse
import sys
import logging
import requests


logger = logging.getLogger(__name__)

class Client:

    def __init__(self, host='127.0.0.1', port=25552):
        """
        Create a client to connect to the KeyValueStore REST Server.

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

        try:
            # Check if the REST API server is running
            requests.get(f'{self.url}/ping')
        except requests.exceptions.ConnectionError:
            # Chances are the REST API server is not
            # running or host/port is incorrect
            print(f"Couldn't connect to {self.host}:{self.port}!",
                  "Make sure the KeyValueStore REST server is running.")
            self.exit(1)
        except Exception as e:
            # Unexpected Error
            logger.exception(e)
            self.exit(1)

    def execute(self, cmd, *args):
        """Execute a command

        :param cmd: Command to be executed
        :type cmd: str
        :return: Result of the command
        :rtype: str
        """
        if cmd.lower() == 'get':
            if len(args) != 1:
                return 'get: Incorrect usage! Expected 1 argument'

            key = args[0]
            response = requests.get(f'{self.url}/{key}')

            if response.status_code == 200  and 'result' in response.json():
                return response.json()['result']
            else:
                logger.error(f'{response.status_code}: {response.text}')
                return 'Unexpected Error!'

        elif cmd.lower() == 'set':
            if len(args) != 2:
                return 'set: Incorrect usage! Expected 2 arguments'

            key, value = args[0], args[1]
            response = requests.post(f'{self.url}/{key}',
                                     json={'value': value})

            if response.status_code == 200  and 'result' in response.json():
                return response.json()['result']
            else:
                logger.error(f'{response.status_code}: {response.text}')
                return 'Unexpected Error!'

        elif cmd.lower() == 'delete':
            if len(args) != 1:
                return 'delete: Incorrect usage! Expected 1 argument'

            key = args[0]
            response = requests.delete(f'{self.url}/{key}')

            if response.status_code == 200 and 'result' in response.json():
                return response.json()['result']
            else:
                logger.error(f'{response.status_code}: {response.text}')
                return 'Unexpected Error!'

        elif cmd.lower() == 'exit':
            self.exit(0)

        else:
            return 'Unrecognized command!'

    def io_loop(self):
        """Run the IO loop to receive input from the user and execute it."""
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