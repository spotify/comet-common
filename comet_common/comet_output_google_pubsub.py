# Copyright 2018 Spotify AB. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines Google PubSub Output Gateway"""
import logging
import json

from google.cloud import pubsub

LOG = logging.getLogger(__name__)


class PubSubOutput:
    """PubSub Output Gateway
        Args:
            topic_name (str): pubsub topic name
    """

    def __init__(self, topic_name):
        """Initialize a PubSubOutput gateway object"""
        self.publisher = pubsub.PublisherClient()
        self.topic_name = topic_name

    def publish_message(self, message, source_type):
        """
        publish message to the output defined topic
        Args:
            message (dict): message dict
            source_type (str): source type of the message
        Raises:
            TypeError: if the message could not be published due to encoding issues
        """
        try:
            message_bytes = self._encode_message(message)

            self.publisher.publish(self.topic_name, message_bytes,
                                   source_type=source_type)
            LOG.debug(f'Publish pubsub message.',
                      extra={'source_type': source_type})
        except TypeError as _:
            LOG.exception('Message processing error')
            LOG.warning(f'Failed publish message: {message} to',
                        extra={'source_type': source_type})

    @staticmethod
    def _encode_message(message):
        """
        Encode message from dict to bytes.
        Args:
            message (dict): message dict
        Returns:
            bytes: the encoded message
        """
        message_str = json.dumps(message)
        message_bytes = message_str.encode("utf-8")
        return message_bytes
