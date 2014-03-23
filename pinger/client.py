#!/usr/bin/env python

import socket
import sys
import time

DEFAULT_PORT = 5005


class UDPPingerClient(object):

    DEFAULT_MESSAGE = 'PING'
    DEFAULT_COUNT = 4
    DEFAULT_SIZE = 1024

    def __init__(self, addr, port):
        """
        :param addr: hostname or IP address of the server
        :param port: UDP port of the server
        """
        ip_addr = socket.gethostbyname(addr)
        self.server_address = (ip_addr, port)
        self.server_name = socket.gethostbyaddr(ip_addr)[0]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1.0)

    def start(self):
        for i in xrange(self.DEFAULT_COUNT):
            try:
                self.socket.sendto(self.DEFAULT_MESSAGE,
                                   self.server_address)
                data = self.socket.recv(self.DEFAULT_SIZE)
                display_name = '%s (%s)' % (self.server_name,
                                            self.server_address[0])
                msg = '%d bytes from %s' % (len(data), display_name)
                self.log_message(msg)
                if i < self.DEFAULT_COUNT - 1:
                    time.sleep(1)

            except socket.timeout:
                msg = 'Request to %s:%d timeout' % self.server_address
                self.log_message(msg)

    def log_message(self, message):
        sys.stderr.write(message + '\n')


if __name__ == '__main__':
    usage = 'Usage: ./client.py <hostname> [port]\n'
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.stderr.write(usage)
        sys.exit(1)
    if len(sys.argv) == 2:
        if sys.argv[1] in ('-h', '--help'):
            sys.stderr.write(usage)
            sys.exit(1)
    addr = sys.argv[1]
    port = DEFAULT_PORT
    if len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            port = int(sys.argv[2])
        else:
            sys.stderr.write('Invalid port number')
            sys.exit(1)
    client = UDPPingerClient(addr, port)
    client.start()
