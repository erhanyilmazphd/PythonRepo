"""
Socket in Python

socket()
send()
recv()
close()
"""
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect( ('data.pr4e.org', 80) )


cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()  # by default encode() uses UTF-8 encoding
my_socket.send(cmd)

while True:
    data = my_socket.recv(512)
    if len(data) < 1:
        break
    print(data.decode(), end='')  # by default decode() uses UTF-8 decoding (to UNICODE)

my_socket.close()