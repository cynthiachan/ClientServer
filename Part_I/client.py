#!/usr/bin/env python
# Author: Cynthia H. Chan
# Echo client program
import socket
import sys

HOST = sys.argv[1]    # The remote host
PORT = int(sys.argv[2])         # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

inputMsg = raw_input('Please enter a message to send to server:')

s.send(inputMsg)
data = s.recv(1024)

print 'Received From Server:', repr(data)

s.close()
