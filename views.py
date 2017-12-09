from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .schema.schema import SchemaGenerator
from .renderers import OpenAPIRenderer, SwaggerUIRenderer


class SwaggerView(APIView):
    # exclude docs view itself from docs
    exclude_from_schema = True

    # get all api class
    permission_classes = [AllowAny]
    renderer_classes = [
        OpenAPIRenderer,
        SwaggerUIRenderer
    ]

    def __init__(self, title='Swagger', endpoints=None, urlpatterns=None,
                 urlconf=None, *args, **kwargs):
        super(SwaggerView, self).__init__(*args, **kwargs)
        self.title = title
        self.endpoints = endpoints
        self.urlpatterns = urlpatterns
        self.urlconf = urlconf

    def get(self, request):
        generator = SchemaGenerator(
            title=self.title,
            endpoints=self.endpoints,
            urlpatterns=self.urlpatterns,
            urlconf=self.urlconf
        )
        if not generator:
            raise ValidationError('Schema generator initialization fail')
        return Response(generator)
