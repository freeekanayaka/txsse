# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET


class EventSourceResource(Resource):
    """SSE endpoint for a browser's EventSource object."""

    isLeaf = True

    def __init__(self, lookupProducer):
        """
        @param lookupProducer: A callable accepting an L{IRequest} object as
            its only argument and returning an L{IPushProducer} (typically
            inheriting from L{EventSourceProducer}) that should write a stream
            of events.
        @type lookupProducer: C{callable}.
        """
        Resource.__init__(self)
        self._lookupProducer = lookupProducer

    def render_GET(self, request):
        request.setHeader("Content-Type", "text/event-stream; charset=utf-8")
        request.setResponseCode(200)
        request.write("")
        producer = self._lookupProducer(request)
        request.registerProducer(producer, 1)
        producer.resumeProducing()
        return NOT_DONE_YET
