from autobahn.twisted.websocket import WebSocketClientProtocol
import json
import datetime

class MyClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        print("opened")
        self.sendMessage(json.dumps({"command": "join", "room": 1}).encode('utf8'))
        self.lc = LoopingCall(self.test_send)
        self.lc.start(5, now=True)

    def test_send(self):
        print("sending message")
        self.sendMessage(json.dumps({"command": "send", "room": 1, "message" : "msg %s" % datetime.datetime.now().isoformat()}).encode('utf8'))
    

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

if __name__ == '__main__':
   import sys

   from twisted.python import log
   from twisted.internet import reactor
   from twisted.internet.task import LoopingCall
   log.startLogging(sys.stdout)

   from autobahn.twisted.websocket import WebSocketClientFactory
   factory = WebSocketClientFactory(url="ws://localhost:8000/chat/stream/")
   factory.protocol = MyClientProtocol

   reactor.connectTCP("127.0.0.1", 8000, factory)
   reactor.run()
