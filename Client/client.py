""" Handling the communication with the client """

from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Communicate:
    """
        Establishes a communication channel between the client and server. Allowing them to send and receive json files.
    """
    def __init__(self):
        self.HEADER = 128
        self.LISTEN_PORT = 5500
        self.HOST = 'localhost'
        self.ADDR = (self.HOST, self.LISTEN_PORT)
        self.SERVER_ADDR = ('localhost', 5005)
        self.FORMAT = 'utf-8'
        self.FILE_NAME_MESSAGE = '<FILE NAME>'
        self.FILE_CONTENTS_MESSAGE = '<FILE CONTENTS>'
        self.DISCONNECT_MESSAGE = '<DISCONNECT>'
        self.listen_host = socket(AF_INET, SOCK_STREAM)
        self.listen_host.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.listen_host.settimeout(0.2)
        self.close = False
        self.listen_thread = []
        self.run_thread = Thread(target=self.run)
        self.run_thread.start()

    def add_padding(self, message):
        """
            Encodes and adds the appropriate padding to a message to match the header size.

            Parameters:
                - message (str) : The message to be padded.

            Returns:
                message (bytes) : The padded message.
        """

        message = message.encode(self.FORMAT)
        message += b' ' * (self.HEADER - len(message))
        return message

    def receive_json(self, connection, address):
        """
            Receives the json file and writes it.

            Parameters:
                - connection (socket) : The connection to the sender.
                - address (tuple(str, int)) : The address to receive from.

            Returns:

        """

        while True:
            message = connection.recv(self.HEADER).decode(self.FORMAT).strip()
            if message == self.DISCONNECT_MESSAGE:
                print(f'[DISCONNECTED] {address}')
                return
            elif message == self.FILE_NAME_MESSAGE:
                print(f'[RECEIVED] {message} from {address}')
                file_name = connection.recv(self.HEADER).decode(self.FORMAT).strip()
            elif message == self.FILE_CONTENTS_MESSAGE:
                file_contents = connection.recv(self.HEADER).decode(self.FORMAT).strip()
                print(f'[RECEIVED] {message} from {address}')

                with open(f'{file_name}.json', 'w') as file:
                    file.write(file_contents)

    def send_json(self, file_name, file_contents):
        """
            Sends a json file to an address.

            Parameters:
                - json_file (str) : The dictionary to be sent.
                - address (tuple(str, int)) : The address to send to.

            Returns:

        """

        send_host = socket(AF_INET, SOCK_STREAM)

        send_host.connect(self.SERVER_ADDR)
        send_host.send(self.add_padding(self.FILE_NAME_MESSAGE))
        send_host.send(self.add_padding(f'{file_name}'))
        send_host.send(self.add_padding(self.FILE_CONTENTS_MESSAGE))
        send_host.send(self.add_padding(f'{file_contents}'))
        send_host.send(self.add_padding(self.DISCONNECT_MESSAGE))
        send_host.close()

    def run(self):
        """
            Starts the listening and handles incoming connections.

            Parameters:
                -

            Returns:

        """

        self.listen_host.bind(self.ADDR)
        self.listen_host.listen()
        print(f'[LISTENING] on (\'{self.HOST}\', {self.LISTEN_PORT})')
        while True:
            if self.close:
                return

            try:
                conn, addr = self.listen_host.accept()
                thread = Thread(target=self.receive_json, args=(conn, addr))
                thread.start()
                self.listen_thread.append(thread)
            except Exception:
                print('[ERROR] incoming connection failed')

    def kill(self):
        """
            Closes the communication.

            Parameters:
                -

            Returns:

        """

        for thread in self.listen_thread:
            thread.join()
        self.listen_host.close()
        self.close = True
        self.run_thread.join()
        print(f'[CLOSED] {self.ADDR}')