# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from testtools.testcase import TestCase

from twisted.web.test.requesthelper import DummyRequest
from twisted.web.server import NOT_DONE_YET

from txsse.producer import EventSourceProducer
from txsse.resource import EventSourceResource


class EventSourceResourceTest(TestCase):

    def setUp(self):
        super(EventSourceResourceTest, self).setUp()
        self.request = DummyRequest([])
        self.resource = EventSourceResource(EventSourceProducer)

    def test_response_headers(self):
        """
        The resource writes the appropriate response headers, according to
        the SSE specification.
        """
        producers = []
        self.request.registerProducer = lambda *args: producers.append(args)
        self.assertIs(NOT_DONE_YET, self.resource.render(self.request))
        [(producer, streaming)] = producers
        self.assertItemsEqual(
            [("Content-Type", ["text/event-stream; charset=utf-8"])],
            self.request.responseHeaders.getAllRawHeaders())
        self.assertEqual(200, self.request.responseCode)
        self.assertEqual(1, streaming)
        self.assertIsInstance(producer, EventSourceProducer)
