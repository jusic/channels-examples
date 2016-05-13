from autobahn.twisted.websocket import WebSocketServerProtocol
import json

class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("connect")
    
    def onOpen(self):
        print("open")

    def onMessage(self, payload, isBinary):
        s = payload.decode('utf8')
        obj = json.loads(payload.decode('utf8'))
        print("received %s" % obj)

    def onClose(self, wasClean, code, reason):
        print("closed: %s" % reason)

if __name__ == '__main__':
    import sys

    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)

    from autobahn.twisted.websocket import WebSocketServerFactory
    factory = WebSocketServerFactory()
    factory.protocol = MyServerProtocol

    reactor.listenTCP(8000, factory)
    reactor.run()
