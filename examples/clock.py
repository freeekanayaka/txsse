import os

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.web.resource import Resource
from twisted.web.static import File

from txsse.resource import EventSourceResource
from txsse.producer import EventSourceProducer


CLOCK_HTML_PATH = os.path.join(os.path.dirname(__file__), "clock.html")


class Clock(EventSourceProducer):

    def resumeProducing(self):
        call = LoopingCall(self._tick)
        call.start(1)

    def _tick(self):
        self.sendMessage(int(reactor.seconds()))


class Root(Resource):

    def __init__(self):
        Resource.__init__(self)
        self.putChild("sse", EventSourceResource(lookupProducer))
        self.putChild("", File(CLOCK_HTML_PATH))


def lookupProducer(request):
    return Clock(request)
