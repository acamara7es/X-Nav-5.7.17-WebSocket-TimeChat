#!/usr/bin/python
# Example WebSocket Server interface
# Original taken from: https://github.com/opiate/SimpleWebSocketServer
# Under the MIT license

import signal
import sys
import ssl
import logging
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from datetime import datetime
from optparse import OptionParser

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

class SimpleEcho(WebSocket):

    def handleMessage(self):
        print self.address, "RECIBIDO => ", self.data
        if self.data is None:
            self.data = ''

        try:
            message = str(self.data)
            print self.address, "ENVIADO => ", message
            self.sendMessage(message)
        except Exception as n:
            print n

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'


class SimpleChat(WebSocket):
    gettime = False
    def handleMessage(self):
        if self.data is None:
            self.data = ''
        elif self.data == "getTime":
            gettime = True
            time = datetime.today()
            self.data = time.strftime("%H:%M:%S %A, %d de %B de %Y")
        for client in self.server.connections.itervalues():
            if client != self or gettime:
                try:
                    client.sendMessage(str(self.address[0]) + ' - ' + str(self.data))
                except Exception as n:
                    print n
        gettime = False
    def handleConnected(self):
        print self.address, 'connected'
        for client in self.server.connections.itervalues():
            if client != self:
                try:
                    client.sendMessage(str(self.address[0]) + ' - connected')
                except Exception as n:
                    print n

    def handleClose(self):
        print self.address, 'closed'
        for client in self.server.connections.itervalues():
            if client != self:
                try:
                    client.sendMessage(str(self.address[0]) + ' - disconnected')
                except Exception as n:
                    print n


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
    parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
    parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
    parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
    parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
    parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

    (options, args) = parser.parse_args()

    cls = SimpleEcho
    if options.example == 'chat':
        cls = SimpleChat

    if options.ssl == 1:
        server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
    else:
        server = SimpleWebSocketServer(options.host, options.port, cls)

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    server.serveforever()
