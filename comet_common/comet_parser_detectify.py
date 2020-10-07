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

"""Representing and (de)serializing events."""

from marshmallow import fields, Schema


class DetectifySchema(Schema):
    """Schema for Detectify"""

    domain = fields.Str(required=True)
    profile_token = fields.Str(required=True)
    scan_token = fields.Str(required=True)
    score = fields.Float(required=False)
    payload = fields.Nested(DetectifyPayloadSchema, required=True)


class DetectifyPayloadSchema(Schema):
    """detectify payload schema class"
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str(required=False)
    report_token = fields.Str(required=True)
    scan_profile_token = fields.Str(required=False)
    signature = fields.Str(required=True)
    url = fields.Str(required=True)
    title = fields.Str(required=True)
    found_at = fields.Str(required=True)
    timestamp = fields.Str(required=False)
    definition = fields.Nested(DetectifyDefinitionSchema, required=True)


class DetectifyDefinitionSchema(Schema):
    """ "detectify definition schema class"
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str(required=False)
    description = fields.Str(required=True)
    risk = fields.Str(required=False)
    references = fields.Nested(DetectifyReferenceSchema(many=True), required=False)


class DetectifyReferenceSchema(Schema):
    """ "detectify reference schema class"
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str(required=False)
    link = fields.Str(required=False)
    name = fields.Str(required=False)
    source = fields.Str(required=False)
