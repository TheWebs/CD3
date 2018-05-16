"""
 Implements a simple HTTP/1.0 Server

"""

import socket

from client_conection import ClientConnection


class Server:

    def __init__(self):
        # Define socket host and port
        self.SERVER_HOST = '0.0.0.0'
        self.SERVER_PORT = 8000

        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))

    def start(self):
        self.server_socket.listen(1)
        print('Listening on port %s ...' % self.SERVER_PORT)
        while True:
            # Wait for client connections
            client_connection, client_address = self.server_socket.accept()
            # Handle client connection
            thread = ClientConnection(client_connection)
            thread.start()
        # Close socket
        server_socket.close()
