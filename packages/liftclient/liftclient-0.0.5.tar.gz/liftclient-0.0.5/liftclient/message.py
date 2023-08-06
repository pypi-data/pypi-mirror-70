from logging import getLogger
from logging import NullHandler

import liftclient.api_pb2


class Message():
    """
        This class represents a Message
    """
    def __init__(
        self,
        value,
        stream,
        key=None,
        ack_inbox=None,
        correlation_id=None,
        offset=None,
        timestamp=None,
        to_partition=None
    ):
        self.logger = getLogger(__name__)
        self.logger.addHandler(NullHandler())
        self.key = key
        self.value = value
        self.stream = stream
        self.ack_inbox = ack_inbox
        self.correlation_id = correlation_id
        self.ack_policy = liftclient.api_pb2.AckPolicy.Value('NONE')
        self.offset = offset
        self.timestamp = timestamp
        self.to_partition = to_partition

    def ack_policy_all(self):
        """Sets the ack policy to wait for all stream replicas to get the message."""
        self.logger.debug('Sets ack policy to wait for all')
        self.ack_policy = liftclient.api_pb2.AckPolicy.Value('ALL')
        return self

    def ack_policy_leader(self):
        """Sets the ack policy to wait for just the stream leader to get the message."""
        self.logger.debug('Sets ack policy to wait the leader')
        self.ack_policy = liftclient.api_pb2.AckPolicy.Value('LEADER')
        return self

    def ack_policy_none(self):
        """Don't send an ack."""
        self.logger.debug('Sets ack policy to no ack')
        self.ack_policy = liftclient.api_pb2.AckPolicy.Value('NONE')
        return self

    def _build_message(self):
        message = self._create_message()
        message.value = str.encode(self.value)
        message.stream = self.stream
        message.ackPolicy = self.ack_policy
        if self.key:
            message.key = str.encode(self.key)
        if self.ack_inbox:
            message.ackInbox = self.ack_inbox
        if self.correlation_id:
            message.correlationId = self.correlation_id
        if self.to_partition:
            message.partition = self.to_partition
        return message

    def _create_message(self):
        return liftclient.api_pb2.Message()

    def __repr__(self):
        return str(self.__dict__)
