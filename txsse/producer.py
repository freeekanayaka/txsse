# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).


class EventSourceProducer(object):
    """Producer writing events on an SSE connection.

    Application code will typically want to sub-class this and override
    at least C{resumeProducing} and typically invoke C{sendMessage} to fire
    messages on the client.
    """

    def __init__(self, request):
        """
        @param request: The L{IRequest} object to send data through.
        """
        self.request = request

    def resumeProducing(self):
        """Resume producing events."""

    def pauseProducing(self):
        """Pause producing events."""

    def stopProducing(self):
        """Stop producing events."""

    def sendMessage(self, data, event=None, id=None):
        """Convenience for sending a message with a single 'data' field."""
        if id:
            self.sendId(id)
        if event:
            self.sendEvent(event)
        self.sendData(data)
        self.sendBlank()

    def sendEvent(self, value):
        """Send an 'event' field identifying the type of message."""
        self._sendField("event", value)

    def sendData(self, value):
        """Send a 'data' field through the stream."""
        self._sendField("data", value)

    def sendId(self, value):
        """Send an 'id' field through the stream."""
        self._sendField("id", value)

    def sendRetry(self, value):
        """Send a 'retry' field through the stream."""
        self._sendField("retry", value)

    def sendBlank(self):
        """Send a blank line, signalling that the message can be fired."""
        self._sendLine("")

    def _sendField(self, field, value):
        self._sendLine("{}: {}".format(field, value))

    def _sendLine(self, text):
        self.request.write("{}\r\n".format(text))
