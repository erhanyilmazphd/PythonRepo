"""
Hyper-Text Transport Protocol (HTTP)

GET:
POST:
Ex: An HTTP Request in Python
"""

import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect( ('data.pr4e.org', 80) )

# Send GET request command
cmd = 'GET http://data.pr4e.org/page1.htm HTTP/1.0\r\n\r\n'.encode()
my_socket.send(cmd)

# Loop till the response is received
while True :
    data = my_socket.recv(512)
    if len(data) < 1 :
        break
    print(data.decode())

# close the socket
my_socket.close()
















