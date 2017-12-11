# DRF Swagger
#### Code Based API document builder

# Overview
- Django Rest Framework (DRF)
- Code Based (Serializer to Docs)
- Swagger UI (https://swagger.io/swagger-ui/)

# Install
0. python2.7

1. install package
```bash
pip install drf_swagger
```
2. add django setting.py INSTALLED_APPS
```python
INSTALLED_APPS = [
    # Your apps
    'rest_framework', # need django rest framework
    'drf_swagger',    # Add drf_swagger
]
```
3. DRF Swagger contains swagger UI static files
```bash
(Your app directory)$ python manage.py collectstatic
```


# Example
```python
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from drf_swagger import drf_request, drf_response

class ViewSetTest(viewsets.ViewSet):
    lookup_field = 'view_set'

    @drf_request(RootSerializer)
    @drf_response(RootSerializer)
    def update(self, request, view_set):
        """
        summary: test summary
        parameters:
            - name: test_param
              in: query
              type: string
              description: Only 'name, in, type' is required
              example: test example
              required: true
        """
        return HttpResponse("!@3123")

class RootSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        help_text='user pk: 46887',
        required=True
    )
    class Meta:
        model = User
        fields = (
            'email',
            'id'
        )
```
![example-img]

# Quick Start

# Warning
- For security, override SwaggerView and add login

# Future Work
- login/security setting
- support python 3

[example-img]: https://github.com/koyouhun/drf_swagger/blob/master/img/web.png?raw=true
