import socket

#LISTA
'''
1- obter recursos (feito)
2- status codes (feito)
3- GET HEAD POST (feito)
4- cabeçalhos (feito)
5- fecho de ligacoes (feito)
6 - caches (feito)
7 - log para ficheiros (nao feito)
'''


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((SERVER_HOST, SERVER_PORT))

client_socket.sendall("etrhdrhtrth / HTTP/1.1".encode())
res = client_socket.recv(1024).decode()
print(res)

# Close socket
client_socket.close()
