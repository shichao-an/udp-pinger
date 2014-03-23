#!/usr/bin/env python

import select
import socket
import sys

DEFAULT_PORT = 5005


class UDPPingerServer(object):

    UDP_IP = ''  # INADDR_ANY

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.server_address = (self.UDP_IP, port)
        self.socket.bind(self.server_address)
        self.socket.setblocking(0)

    def start(self):
        msg = 'Starting ping server at 0.0.0.0:%d\n' % self.server_address[1]
        sys.stderr.write(msg)
        while True:
            r, w, e = select.select([self.socket.fileno()], [], [], 1)
            if self.socket.fileno() in r:
                data, addr = self.socket.recvfrom(1024)
                self.log_message(addr)
                self.socket.sendto(data, addr)

    def log_message(self, addr):
        msg = 'Ping from %s:%d\n' % addr
        sys.stderr.write(msg)


if __name__ == '__main__':
    usage = 'Usage: ./server.py [port]\n'
    port = DEFAULT_PORT
    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            port = int(sys.argv[1])
        elif sys.argv[1] in ('-h', '--help'):
            sys.stderr.write(usage)
            sys.exit(1)
        else:
            sys.stderr.write('Invalid port number')
            sys.exit(1)
    if len(sys.argv) > 2:
        sys.stderr.write(usage)
        sys.exit(1)
    server = UDPPingerServer(port)
    server.start()
