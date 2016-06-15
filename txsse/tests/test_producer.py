# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from testtools.testcase import TestCase

from twisted.web.test.requesthelper import DummyRequest

from txsse.producer import EventSourceProducer


class EventSourceProducerTest(TestCase):

    def setUp(self):
        super(EventSourceProducerTest, self).setUp()
        self.request = DummyRequest([])
        self.producer = EventSourceProducer(self.request)

    def test_sendMessage(self):
        """
        Send a message with a single data field.
        """
        self.producer.sendMessage("hello")
        self.assertEqual(["data: hello\r\n", "\r\n"], self.request.written)

    def test_sendMessage_with_event_type(self):
        """
        Send a message with an event type.
        """
        self.producer.sendMessage("hello", event="greeting")
        self.assertEqual(
            ["event: greeting\r\n", "data: hello\r\n", "\r\n"],
            self.request.written)

    def test_sendMessage_with_id(self):
        """
        Send a message with an ID.
        """
        self.producer.sendMessage("hello", id="123")
        self.assertEqual(
            ["id: 123\r\n", "data: hello\r\n", "\r\n"],
            self.request.written)

    def test_sendRetry(self):
        """
        Send a retry field.
        """
        self.producer.sendRetry("120")
        self.assertEqual(["retry: 120\r\n"], self.request.written)
