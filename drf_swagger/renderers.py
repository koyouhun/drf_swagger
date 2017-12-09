from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BaseRenderer, JSONRenderer


class OpenAPIRenderer(BaseRenderer):
    media_type = 'application/openapi+json'
    format = 'openapi'
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code != 200:
            # Error report
            return JSONRenderer().render(data)

        schema = data.swagger_schema
        if schema is None:
            raise ValidationError('Schema generation fail')
        return JSONRenderer().render(schema)


class SwaggerUIRenderer(BaseRenderer):
    media_type = 'text/html'
    format = 'swagger'
    template = 'index.html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return render(
            renderer_context['request'],
            self.template,
            renderer_context
        )
