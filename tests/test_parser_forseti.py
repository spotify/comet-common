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

"""Test comet_parser_forseti module"""


from comet_common.comet_parser_forseti import ForsetiSchema, SUPPORTED_RESOURCE_TYPES, SUPPORTED_RESOURCE
from marshmallow import ValidationError

_payload_ForsetiSchema = dict(
    id=0,
    project_id="",
    project_owner="",
    resource=None,
    resource_id="",
    resource_type=None,
    violation_data=dict(resource="", violation_data=dict()),
)


def test_ForsetiSchema_parsedok():
    payload_ForsetiSchema = dict(_payload_ForsetiSchema)
    for srt in SUPPORTED_RESOURCE_TYPES:
        for sr in SUPPORTED_RESOURCE:
            payload_ForsetiSchema["resource"] = sr
            payload_ForsetiSchema["resource_type"] = srt
            payload_ForsetiSchema["violation_data"] = dict([(k, "") for k in SUPPORTED_RESOURCE[sr]])
            assert ForsetiSchema().validate(payload_ForsetiSchema) == {}


def test_ForsetiSchema_fail():
    payload_ForsetiSchema = dict(_payload_ForsetiSchema)
    err = ForsetiSchema().validate(payload_ForsetiSchema)
    assert "Field may not be null." in err.get("resource")
    assert "Field may not be null." in err.get("resource_type")
    assert "Forseti requires resource field" in err.get("resource")

    payload_ForsetiSchema["resource"] = list(SUPPORTED_RESOURCE.keys())[0]
    err = ForsetiSchema().validate(payload_ForsetiSchema)
    assert "Field may not be null." in err.get("resource_type")
    assert "Forseti requires resource_type field" in err.get("resource_type")

    payload_ForsetiSchema["resource_type"] = SUPPORTED_RESOURCE_TYPES[0]
    err = ForsetiSchema().validate(payload_ForsetiSchema)
    assert "violation_data" in err
