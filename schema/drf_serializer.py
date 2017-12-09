# -*- coding:utf-8 -*-

from django.utils.encoding import force_text
from rest_framework import fields, serializers
import rest_framework
if rest_framework.VERSION >= '3.0.0':
    from rest_framework.fields import empty
else:
    class empty:
        pass


def get_serializer_fields(serializer):
    """
    Convert Django REST Framework serializer to OpenAPI formed dict
    :param serializer: Django REST Framework serializer
    :return: OpenAPI definition formed dict
    """

    # If not serializer, return empty dict
    if isinstance(serializer, serializers.SerializerMetaclass):
        serializer = serializer()
    if not isinstance(serializer, serializers.Serializer):
        return dict()

    # Get serializer's name
    serializer_name = serializer.__class__.__name__

    # Get serializer's fields
    if not hasattr(serializer, 'get_fields'):
        return dict()
    else:
        serializer_fields = serializer.get_fields()

    # Set initial data
    ret = dict()
    ret_fields = dict()
    ret_required = list()

    # populate data
    for name, field in serializer_fields.items():
        field_type, field_format = get_field_type(field)

        #####
        # Special Case
        #####
        # Hidden Field (Ignore)
        if field_type == 'hidden':
            continue

        # Nested Serializer (Recursion)
        elif field_type == 'serializer':
            # if list serializer, get normal serializer
            if field_format == 'list':
                field = field.child

            # Fill Definitions
            inner_fields, inner_serializer_name = get_serializer_fields(field)
            ret.update(inner_fields)

            # Fill Required
            required = getattr(field, 'required', True)
            if required:
                ret_required.append(name)

            # Fill Field
            field = {'$ref': '#definitions/'+inner_serializer_name}
            ret_fields[name] = field
            continue

        # Choice (collect data, set field_type)
        choices = []
        if field_type == 'choice':
            if isinstance(field.choices, list):
                choices = [k for k, v in field.choices]
            elif isinstance(field.choices, dict):
                choices = [k for k, v in field.choices.items()]
            field_type, field_format = get_choice_type(choices)

        #####
        # Normal Case
        #####
        description = getattr(field, 'help_text', None)
        if description:
            description = force_text(description)

        # TODO: Check None works properly
        example = getattr(field, 'default', empty)

        required = getattr(field, 'required', True)
        if required:
            ret_required.append(name)
        field = {
            'description': description,
            'type': field_type,
            'format': field_format,
            'example': example
        }

        if not field['description']:
            del field['description']
        if field['type'] == field['format']:
            del field['format']
        if field['example'] is empty:
            del field['example']

        # Min/Max values
        max_value = getattr(field, 'max_value', None)
        min_value = getattr(field, 'min_value', None)
        if max_value is not None and field_type == 'integer':
            field['minimum'] = min_value

        if max_value is not None and field_type == 'integer':
            field['maximum'] = max_value

        # ENUM options
        if choices:
            field['enum'] = choices

        # Fill Field
        ret_fields[name] = field

    ret.update({
        serializer_name: {
            'type': 'object',
            'required': ret_required,
            'properties': ret_fields
        }
    })

    return ret, serializer_name


def get_field_type(field):
    if isinstance(field, fields.BooleanField):
        return 'boolean', 'boolean'
    elif isinstance(field, fields.NullBooleanField):
        return 'boolean', 'boolean'
    elif isinstance(field, fields.ChoiceField):
        return 'choice', 'choice'
    elif isinstance(field, fields.DateField):
        return 'string', 'date'
    elif isinstance(field, fields.DateTimeField):
        return 'string', 'date-time'
    elif isinstance(field, fields.IntegerField):
        return 'integer', 'int64'
    elif isinstance(field, fields.FloatField):
        return 'number', 'float'
    elif isinstance(field, fields.HiddenField):
        return 'hidden', 'hidden'
    elif isinstance(field, fields.ListField):
        return 'array', 'array'
    elif isinstance(field, serializers.Serializer):
        return 'serializer', 'serializer'
    elif isinstance(field, serializers.ListSerializer):
        return 'serializer', 'list'
    else:
        return 'string', 'string'


def get_choice_type(choices):
    if len(choices) == 0:
        return 'string', 'string'
    else:
        choice = choices[0]

    if isinstance(choice, bool):
        return 'boolean', 'boolean'
    elif isinstance(choice, int):
        return 'integer', 'int32'
    elif isinstance(choice, float):
        return 'number', 'float'
    else:
        return 'string', 'string'
