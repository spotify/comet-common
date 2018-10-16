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

"""Test comet_input_google_pubsub module"""

from unittest.mock import patch, Mock
import pytest

from comet_common.comet_input_google_pubsub import PubSubInput

def test_input_google_pubsub_passingok():
    """PubSubInput"""
    with patch("comet_common.comet_input_google_pubsub.pubsub.SubscriberClient") as mockpubsub:
        mockpubsub().subscribe.return_value = None
        message_callback = Mock(return_value=True)
        pubsubinput = PubSubInput(message_callback=message_callback, subscription_name="something")
        message = Mock()
        message.attributes.get.return_value = 'test_type'
        
        message.data.decode.return_value = '{}'
        pubsubinput.callback(message)
        message.ack.assert_called_once()
        message_callback.assert_called_once()


def test_input_google_pubsub_failingtodecode():
    """PubSubInput"""
    with patch("comet_common.comet_input_google_pubsub.pubsub.SubscriberClient") as mockpubsub:
        mockpubsub().subscribe.return_value = None

        message_callback = Mock(return_value=False)
        pubsubinput = PubSubInput(message_callback=message_callback, subscription_name="something")
        message = Mock()
        message.attributes.get.return_value = 'test_type'

        message.data.decode.side_effect = Exception("Mock Exception")
        with pytest.raises(Exception) as excinfo:
            pubsubinput.callback(message)
        assert excinfo.value.args[0] == 'Mock Exception'
        message.nack.assert_called_once()


def test_input_google_pubsub_nocallback():
    """PubSubInput"""
    with patch("comet_common.comet_input_google_pubsub.pubsub.SubscriberClient") as mockpubsub:
        mockpubsub().subscribe.return_value = None
        message_callback = Mock(return_value=False)
        pubsubinput = PubSubInput(message_callback=message_callback, subscription_name="something")
        message = Mock()
        message.attributes.get.return_value = 'test_type'

        message.data.decode.side_effect = '{}'
        pubsubinput.callback(message)
        message.nack.assert_called_once()

def test_input_google_pubsub_stop():
    with patch("comet_common.comet_input_google_pubsub.pubsub.SubscriberClient") as mockpubsub:
        mockpubsub().subscribe.return_value = None
        message_callback = Mock(return_value=False)
        pubsubinput = PubSubInput(message_callback=message_callback, subscription_name="something")
        pubsubinput.consumer = Mock()
        pubsubinput.stop()
        pubsubinput.consumer.cancel.assert_called_once()


