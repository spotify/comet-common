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


class DetectifyPayloadHighlightsSchema(Schema):
    """DetectifyPayloadHighlightsSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    field = fields.Str()
    offset = fields.Int()
    length = fields.Int()


class DetectifyPayloadTargetResponseheadersSchema(Schema):
    """DetectifyPayloadTargetResponseheadersSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    name = fields.Str()
    value = fields.Str()


class DetectifyPayloadTargetRequestheadersSchema(Schema):
    """DetectifyPayloadTargetRequestheadersSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    name = fields.Str()
    value = fields.Str()


class DetectifyPayloadTargetSchema(Schema):
    """DetectifyPayloadTargetSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    type_field = fields.Str(data_key="type")
    url = fields.Str()
    request_method = fields.Str()
    request_version = fields.Str()
    request_headers = fields.Nested(DetectifyPayloadTargetRequestheadersSchema(many=True))
    request_body = fields.Str()
    request_body_base64 = fields.Bool()
    response_status_code = fields.Int()
    response_reason_phrase = fields.Str()
    response_version = fields.Str()
    response_headers = fields.Nested(DetectifyPayloadTargetResponseheadersSchema(many=True))
    response_body = fields.Str()
    response_body_base64 = fields.Bool()
    response_encoding = fields.Str()


class DetectifyPayloadTagsSchema(Schema):
    """DetectifyPayloadTagsSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    type_field = fields.Str(data_key="type")
    value = fields.Str()


class DetectifyPayloadScoreSchema(Schema):
    """DetectifyPayloadScoreSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    version = fields.Str()
    score = fields.Float()
    vector = fields.Str()


class DetectifyReferenceSchema(Schema):
    """ "detectify reference schema class"
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    link = fields.Str()
    name = fields.Str()
    source = fields.Str()


class DetectifyDefinitionSchema(Schema):
    """DetectifyDefinitionSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    description = fields.Str(required=True)
    risk = fields.Str()
    references = fields.Nested(DetectifyReferenceSchema(many=True))


class DetectifyPayloadDetailsSchema(Schema):
    """DetectifyPayloadDetailsSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    name = fields.Str()
    type_field = fields.Str(data_key="type")
    uuid = fields.Str()
    value = fields.Str()


class DetectifyPayloadOwaspSchema(Schema):
    """DetectifyPayloadOwaspSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    classification = fields.Str()
    year = fields.Int()


class DetectifyPayloadVulnerableVariableSchema(Schema):
    """DetectifyPayloadVulnerableVariableSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    name = fields.Str()
    method = fields.Str()


class DetectifyPayloadHeaderSchema(Schema):
    """DetectifyPayloadHeaderSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    name = fields.Str()
    direction = fields.Str()
    value = fields.Str()


class DetectifyPayloadVulnerableResourcesSchema(Schema):
    """DetectifyPayloadVulnerableResourcesSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    expected_header = fields.Nested(DetectifyPayloadHeaderSchema(many=True))
    vulnerable_header = fields.Nested(DetectifyPayloadHeaderSchema(many=True))
    vulnerable_variable = fields.Nested(DetectifyPayloadVulnerableVariableSchema(many=True))


class DetectifyPayloadSchema(Schema):
    """DetectifyPayloadSchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    uuid = fields.Str()
    report_token = fields.Str(required=True)
    scan_profile_token = fields.Str()
    signature = fields.Str(required=True)
    url = fields.Str(required=True)
    title = fields.Str(required=True)
    found_at = fields.Str(required=True)
    timestamp = fields.Str()
    definition = fields.Nested(DetectifyDefinitionSchema, required=True)
    score = fields.Nested(DetectifyPayloadScoreSchema(many=True))
    cwe = fields.Int()
    tags = fields.Nested(DetectifyPayloadTagsSchema(many=True))
    target = fields.Nested(DetectifyPayloadTargetSchema)
    highlights = fields.Nested(DetectifyPayloadHighlightsSchema(many=True))
    details = fields.Nested(DetectifyPayloadDetailsSchema(many=True))
    owasp = fields.Nested(DetectifyPayloadOwaspSchema(many=True))
    vulnerable_resources = fields.Nested(DetectifyPayloadVulnerableResourcesSchema)


class DetectifySchema(Schema):
    """DetectifySchema schema class
    Args:
        Schema (marshmallow.Schema): schema
    """

    domain = fields.Str(required=True)
    domain_token = fields.Str(allow_none=True)
    profile_token = fields.Str(required=True)
    scan_token = fields.Str(required=True)
    score = fields.Float()
    severity_score = fields.Float()
    payload = fields.Nested(DetectifyPayloadSchema, required=True)
