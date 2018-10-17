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

from marshmallow import fields, Schema, validate, validates_schema, ValidationError

SUPPORTED_RESOURCE_TYPES = [
    'bucket',
    'project',
    'cloudsql',
    'bigquery_dataset'
]

# Supported resource and their required fields
SUPPORTED_RESOURCE = {
    'policy_violations': ['member', 'role'],
    'buckets_acl_violations': ['bucket', 'entity', 'role'],
    'cloudsql_acl_violations': ['instance_name'],
    'bigquery_acl_violations': ['dataset_id']
}


class ForsetiSchema(Schema):
    """Schema for Forseti"""
    id = fields.Int(required=True)
    project_id = fields.Str(required=True)
    project_owner = fields.Str(required=True, allow_none=True)
    resource = fields.Str(required=True, validate=validate.OneOf(SUPPORTED_RESOURCE.keys()))
    resource_id = fields.Str(required=True)
    resource_type = fields.Str(required=True, validate=validate.OneOf(SUPPORTED_RESOURCE_TYPES))
    violation_data = fields.Dict(required=True)

    @validates_schema
    def validate_violation_data(self, data):  # pylint: disable=no-self-use
        """Validate that violation_data has the field we expect depending on the resource field.
        Args:
            data (dict): the data object
        Raises:
            ValidationError: if the violation_data has insufficient fields for the resource,
                             or resource_type or resource are not provided
        """

        if 'resource' not in data.keys():
            raise ValidationError('Forseti requires resource field', ['resource'])

        if 'resource_type' not in data.keys():
            raise ValidationError('Forseti requires resource_type field', ['resource_type'])

        resource = data['resource']

        for field in SUPPORTED_RESOURCE.get(resource):
            if field not in data['violation_data']:
                raise ValidationError(f'{resource} resource requires member field {field} in violation_data',
                                      ['violation_data'])
