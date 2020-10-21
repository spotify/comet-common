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

"""Test comet_parser_detectify module"""

from comet_common.comet_parser_detectify import DetectifyDefinitionSchema, DetectifyPayloadSchema, DetectifySchema

payload_ReferenceSchema = [dict(uuid="", link="", name="", source="")]
payload_DetectifyDefinitionSchema = dict(description="", references=payload_ReferenceSchema)
payload_DetectifyPayloadSchema = dict(
    signature="", url="", title="", found_at="", report_token="", definition=payload_DetectifyDefinitionSchema
)
payload_DetectifySchema = dict(scan_token="", profile_token="", domain="", payload=payload_DetectifyPayloadSchema)
payload_DetectifySchema_complete = {**payload_DetectifySchema, "score": 7.1}


def test_DetectifyDefinitionSchema():
    assert DetectifyDefinitionSchema().validate(payload_DetectifyDefinitionSchema) == {}
    assert "description" in DetectifyDefinitionSchema().validate({})


def test_DetectifyPayloadSchema():
    assert DetectifyPayloadSchema().validate(payload_DetectifyPayloadSchema) == {}
    for k in payload_DetectifyPayloadSchema:
        assert k in DetectifyPayloadSchema().validate({})


def test_DetectifySchema():
    assert DetectifySchema().validate(payload_DetectifySchema) == {}
    for k in payload_DetectifySchema:
        assert k in DetectifySchema().validate({})
    assert DetectifySchema().validate(payload_DetectifySchema_complete) == {}
    assert "score" not in DetectifySchema().validate({})
