# -*- coding:utf-8 -*-

from .endpoint import get_endpoints
from .view_info import ViewInfoReader
from drf_swagger.utils.url_path import get_prefix, get_common_path


class SchemaGenerator(object):
    def __init__(self, title="Swagger", version="", urlconf=None,
                 urlpatterns=None, endpoints=None):
        self.title = title
        self.version = version
        self.endpoints = get_endpoints(urlconf, urlpatterns, endpoints)
        self.schema = dict()
        self.definitions = dict()
        self.populate_schema()

    @property
    def swagger_schema(self):
        """
        API schema in dict
        """
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "contact": {
                    "name": "drf_swagger",
                    "url": "https://github.com/koyouhun/swagger_test"
                }
            },
            "paths": self.schema,
            "definitions": self.definitions
        }

    def populate_schema(self):
        """
        Populate API Schema
        """
        paths = [path for path, m, v in self.endpoints]
        common_path = get_common_path(get_prefix(paths))

        for path, method, callback in self.endpoints:
            reader = ViewInfoReader(common_path, path, method, callback)
            view_info = reader.view_info
            view_definitions = reader.definitions

            if path in self.schema:
                self.schema[path][method.lower()] = view_info
            else:
                self.schema[path] = {method.lower(): view_info}
            self.definitions.update(view_definitions)
