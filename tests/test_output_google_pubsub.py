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

"""Test comet_output_google_pubsub module"""

from unittest.mock import patch, MagicMock
import pytest

from comet_common.comet_output_google_pubsub import PubSubOutput
publisher_client_path = \
    'comet_common.comet_output_google_pubsub.pubsub.PublisherClient'


def test_output_google_pubsub_passing_ok():
    """PubSubOutput"""
    with patch(publisher_client_path) as mockpubsub:
        mockpubsub().publish.return_value = None

        pubsub_output = PubSubOutput("some topic")
        pubsub_output._encode_message = MagicMock()
        pubsub_output._encode_message.return_value = \
            '''{'message': 'content'}'''
        message = {'message': 'content'}

        pubsub_output.publish_message(message, 'source_type')

        pubsub_output._encode_message.assert_called_once()
        mockpubsub().publish.assert_called_once()


def test_output_google_pubsub_failing_to_encode():
    """PubSubOutput"""
    with patch(publisher_client_path) as mockpubsub:
        pubsub_output = PubSubOutput("some topic")
        pubsub_output._encode_message = MagicMock()
        pubsub_output._encode_message.side_effect = \
            Exception("Encode Exception")
        message = {'message': 'content'}

        with pytest.raises(Exception) as excinfo:
            pubsub_output.publish_message(message, 'source_type')

        assert excinfo.value.args[0] == 'Encode Exception'
        mockpubsub().publish.assert_not_called()


def test_output_google_pubsub_failing_to_publish():
    """PubSubInput"""
    with patch(publisher_client_path) as mockpubsub:
        mockpubsub().publish.side_effect = \
            Exception("PubSub Publish Exception")

        pubsub_output = PubSubOutput("some topic")
        pubsub_output._encode_message = MagicMock()
        pubsub_output._encode_message.return_value = \
            '''{'message': 'content'}'''
        message = {'message': 'content'}

        with pytest.raises(Exception) as excinfo:
            pubsub_output.publish_message(message, 'source_type')

        assert excinfo.value.args[0] == "PubSub Publish Exception"
        pubsub_output._encode_message.assert_called_once()


def test_encode_message_success():
    """Test encoding message works"""
    pubsub_output = PubSubOutput("some topic")
    message = {'message': 'content'}
    expected = b'{"message": "content"}'
    actual = pubsub_output._encode_message(message)
    assert actual == expected
