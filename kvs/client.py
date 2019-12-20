import socket
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

class Client:

    def __init__(self, host='127.0.0.1', port=25552, size=1024):
        """
        Creates a client to connect to the KeyValueStore Server.

        :param host: The host address to connect to, defaults to 127.0.0.1
        :type host: str, optional
        :param port: The port the server is running on, defaults to 25552
        :type host: int, optional
        :param size: The buffer size of data to receive
        :type size: int, optional
        """
        self.host = host
        self.port = port
        self.size = size

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except ConnectionRefusedError:
            logger.error(f'Could not connect to {self.host}:{self.port}')
            self.close()
            sys.exit(1)
        except Exception as e:
            logger.exception(e)
            self.close()
            sys.exit(1)

    def io_loop(self):
        """Begins the IO loop allowing you to send/receive data to and from the server."""
        while True:
            try:
                inp = input('> ')

                self.sock.sendall(inp.encode())
                response = self.sock.recv(self.size).decode()

                if inp.lower() == 'exit':
                    self.close()

                print(response)

            except (KeyboardInterrupt, EOFError):
                self.close()
                return
            except Exception as e:
                self.close()
                logger.exception(e)
                return

    def close(self):
        """Close the socket connection to the server."""
        self.sock.close()
        sys.exit(0)

if __name__ == "__main__":
    client = Client()
    client.io_loop()