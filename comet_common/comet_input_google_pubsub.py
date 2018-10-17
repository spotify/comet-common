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

"""Defines Google PubSub Input Gateway"""
import logging

from google.cloud import pubsub
from comet_core.plugin_interface import CometInput

LOG = logging.getLogger(__name__)


class PubSubInput(CometInput):
    """PubSub Input Gateway
        Args:
            message_callback (function): callback function
            subscription_name (str): pubsub subscription name
        """

    def __init__(self, message_callback, subscription_name):
        """Initialize a PubSubInput gateway object"""
        super().__init__(message_callback)

        subscriber = pubsub.SubscriberClient()
        self.consumer = subscriber.subscribe(subscription_name, self.callback)

    def callback(self, message):
        """
        Callback function that puts a consumed message in the self.messages queue.
        Args:
            message (google.cloud.pubsub_v1.subscriber.message.Message): message object
        Raises:
            Exception: if smth happens (sorry)
        """
        try:
            source_type = message.attributes.get('source_type', None)
            LOG.debug(f'Received pubsub message.', extra={'source_type': source_type})
            data = message.data.decode()
            if self.message_callback(source_type, data):
                LOG.debug(f'Acknowledge pubsub message.', extra={'source_type': source_type})
                message.ack()
                return
        except Exception as _:
            LOG.exception('Message processing error')
            LOG.warning(f'Refused (nacked) pubsub message.', extra={'source_type': source_type})
            message.nack()
            raise
        LOG.warning(f'Refused (nacked) pubsub message.', extra={'source_type': source_type})
        message.nack()

    def stop(self):
        self.consumer.cancel()
