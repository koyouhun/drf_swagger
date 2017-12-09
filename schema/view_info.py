# -*- coding:utf-8 -*-

import yaml
import uritemplate
import rest_framework

from drf_swagger.utils.url_path import get_prefix
from drf_swagger.utils.data_type import get_type_format, str_to_type

from .utils import get_func_from_callback
from .drf_serializer import get_serializer_fields


class ViewInfoReader(object):
    """
    View Information Reader for Swagger(OpenAPI)
    target: YAML, serializer(Django REST Framework)
    """

    def __init__(self, common_path, path, method, callback):
        """
        parameters
        - callback: view callback of endpoint(urlpattern)
        - method: get, post, ...
        """
        self.operationId = str(path) + str(method)
        prefix = get_prefix(path[len(common_path):]).strip('/')
        self.tag = [t for t in prefix.split('/') if t]
        self.view_info, self.definitions = self.get_schema(
            self.read_view_info(path, method, callback))

    def get_schema(self, view_info):
        ret = {
            'operationId': self.operationId,
            'responses': view_info.get('responses', None) or {"200": {}}
        }
        if self.tag:
            ret['tags'] = [self.tag]
        if view_info.get('summary', False):
            ret['summary'] = view_info['summary']
        if view_info.get('description', False):
            ret['description'] = view_info['description']
        if view_info.get('fields', False):
            ret['parameters'] = view_info['fields']
        if view_info.get('requestBody', False):
            ret['requestBody'] = view_info['requestBody']
        return ret, (view_info['definitions'] or dict())

    def read_view_info(self, path, method, callback):
        # make basic data
        func = get_func_from_callback(method, callback)
        fields = list()
        definitions = dict()
        if func:
            docs = self.get_doc(func)

            # get fields, definitions

            # from path
            fields += self.path_reader(path)
            # from view function docs
            if docs:
                summary = docs.get('summary', None)
                description = docs.get('description', None)
                docs_fields = self.docs_parameter_reader(docs)
            else:
                summary = None
                description = None
                docs_fields = list()

            # join fields
            for i in range(len(fields)):
                for d in docs_fields:
                    if fields[i]['name'] == d['name']:
                        fields[i].update(d)
                        break
                    else:
                        fields.append(d)

            # from drf_request
            refs, root_name = self.drf_data_reader(func, 'drf_request')
            if refs:
                request_body = {
                    "description": root_name,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": '#definitions/' + root_name
                             }}}}
                definitions.update(refs)
            else:
                request_body = None

            # from drf_response
            refs, root_name = self.drf_data_reader(func, 'drf_response')
            if refs:
                responses = {
                    "200": {
                        "description": root_name,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#definitions/' + root_name
                                }}}}}
                definitions.update(refs)
            else:
                responses = None

        else:
            summary = None
            description = None
            request_body = None
            responses = None

        return {
            "summary": summary,
            "description": description,
            "fields": fields,
            "requestBody": request_body,
            "responses": responses,
            "definitions": definitions
        }

    @staticmethod
    def get_doc(func):
        if func is None:
            return dict()

        doc = getattr(func, '__doc__', None)
        if doc is None:
            return dict()

        doc = yaml.load(doc)
        if not isinstance(doc, dict):
            doc = {'summary': doc}
        return doc

    @staticmethod
    def path_reader(path):
        fields = list()
        for variable in uritemplate.variables(path):
            field = {'name': variable,
                     'in': 'path',
                     'required': True,
                     'schema': {'type': 'string'}}
            fields.append(field)
        return fields

    @staticmethod
    def docs_parameter_reader(docs):
        fields = list()

        parameters = docs.get('parameters', None)
        if parameters is None:
            return fields

        for param in parameters:
            # get required data
            p_in = param.get('in', None)
            p_name = param.get('name', None)
            p_type = param.get('type', None)

            # Filtering invalid input
            if not (p_in and p_name and p_type):
                continue
            p_type, p_format = get_type_format(p_type)
            if p_type in ['array', 'choice']:
                # TODO: future support
                continue

            # get optional data
            p_required = str_to_type(param.get('required', True), 'boolean')
            p_description = param.get('description', None)
            p_example = str_to_type(param.get('default', None), p_type)

            # make field
            field = {
                # required
                'in': p_in,
                'name': p_name,
                'schema': {
                    'type': p_type,
                    'format': p_format
                },

                # For swagger, required
                # For user, optional
                'required': p_required,

                # optional
                'description': p_description,
                'example': p_example
            }
            if field['schema']['type'] == field['schema']['format']:
                del field['schema']['format']
            if p_required is None:
                field['required'] = True
            if p_example is None:
                del field['example']
            if field['description'] is None:
                del field['description']
            fields.append(field)

        return fields

    @staticmethod
    def drf_data_reader(func, name):
        drf_data = getattr(func, name, None)

        # Django REST Framework serializer
        if isinstance(drf_data, rest_framework.serializers.SerializerMetaclass):
            return get_serializer_fields(drf_data)
        else:
            return dict(), ""
