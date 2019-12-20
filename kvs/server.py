import logging
import socket
import threading

from kvs.kvs import KeyValueStore


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Server:

    def __init__(self, host='127.0.0.1', port=25552, max_clients=4, size=1024):
        """Creates a server instance of KeyValueStore

        :param host: The host address to run the server on, defaults to '127.0.0.1'
        :type host: str, optional
        :param port: The port to run the server on, defaults to 25552
        :type port: int, optional
        :param max_clients: The max number of clients to accept, defaults to 4
        :type max_clients: int, optional
        :param size: The buffer size to receive data
        :type size: int, optional
        """
        self.kv = KeyValueStore()
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.size = size
        self.lock = threading.RLock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

    def listen(self):
        """Begins the servers' listening process."""
        self.sock.listen(self.max_clients)
        logger.info(f'Server listening on {self.host}:{self.port}')

        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.handle_client,
                             args=(client, address)).start()

    def handle_client(self, client, address):
        """Handles a client

        :param client: A socket object representing the
        :type client: `socket.socket`
        :param address: Address of the client
        :type address: tuple
        """
        logger.info(f'Connection Received: {address[0]}:{address[1]}')
        while True:
            try:
                data = client.recv(self.size)
                if data:
                    response = self.handle_request(data)
                    client.sendall(response.encode())
                else:
                    logger.info(f'Client {address[0]}:{address[1]} disconnected')
                    client.close()
            except Exception:
                client.close()
                return

    def handle_request(self, data):
        """Handles a request from the client

        :param data: Data representing the request
        :type data: bytes
        :return: A response to the request
        :rtype: str
        """
        self.lock.acquire()

        data = data.decode()
        response = self.execute(*data.split())

        self.lock.release()
        return response

    def execute(self, cmd, *args):
        """Executes the command specified by cmd

        :param cmd: The command to be executed
        :type cmd: str
        :return: The result of the command
        :rtype: str
        """
        if cmd.lower() == 'get':
            if len(args) != 1:
                return 'GET: Incorrect Usage! Specify 1 argument'

            resp = self.kv.get(args[0])
            if resp:
                return resp
            else:
                return 'null'

        elif cmd.lower() == 'set':
            if len(args) != 2:
                return 'SET: Incorrect Usage! Specify 2 arguments'

            resp = self.kv.set(args[0], args[1])
            if resp:
                return f'{args[0]}:{args[1]} stored successfully'
            else:
                return f'{args[0]}:{args[1]} error storing'

        elif cmd.lower() == 'delete':
            if len(args) != 1:
                return 'DELETE: Incorrect Usage! Specify 1 argument'
            resp = self.kv.delete(args[0])
            if resp:
                return f'{args[0]} deleted'
            else:
                return f'{args[0]} does not exist'

        else:
            return 'Unrecognized Command'

    def close(self):
        """Closes the server."""
        # TODO Handle close server when clients are still connected
        logger.info('Closing Server')
        self.sock.close()

def main():
    server = Server()

    try:
        server.listen()
    except (KeyboardInterrupt, EOFError):
        server.close()
    except Exception as e:
        logger.exception(e)
        server.close()

if __name__ == "__main__":
    main()