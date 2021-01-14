#!/usr/bin/python

# Make sure to have the simpleTe running

import sys
import socket
import time

def client(message):
    host = '127.0.0.1'
    port = 12345  # Make sure it's within the > 1024 $$ <65535 range
    s = socket.socket()
    s.connect((host, port))
    s.send(str(message).encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    #print('Received from server: ' + data)
    s.close()

def readdata(file):
    f=open(file)
    lines=f.readlines()
    client(lines[0])
    #print(lines[0])
    time.sleep(0.5)


if __name__ == '__main__':

    files = ['examples/uav/data/positions_1.txt', 'examples/uav/data/positions_2.txt','examples/uav/data/positions_3.txt']
    while True:
        for x in files:
            readdata(x)
