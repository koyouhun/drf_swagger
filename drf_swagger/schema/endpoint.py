# -*- coding:utf-8 -*-

from importlib import import_module
from django.conf import settings
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from .utils import urlregex_to_path, get_methods, is_rest_framework_view


def get_urlpatterns(urlconf):
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF

    if isinstance(urlconf, str):
        return import_module(urlconf).urlpatterns
    else:
        return urlconf.urlpatterns


def get_endpoints(urlconf, urlpatterns, endpoints):
    return endpoints or _get_endpoints(urlpatterns or get_urlpatterns(urlconf))


def _get_endpoints(urlpatterns, prefix=''):
    endpoints = list()
    for urlpattern in urlpatterns:
        pattern = urlregex_to_path(urlpattern.regex.pattern)
        while prefix.endswith('/') and pattern.startswith('/'):
            prefix = prefix[:-1]
        path = prefix + pattern
        if isinstance(urlpattern, RegexURLPattern):
            callback = urlpattern.callback
            if not is_rest_framework_view(callback):
                continue
            if getattr(callback.cls(), 'exclude_from_schema', False):
                continue
            for method in get_methods(callback):
                endpoints.append((path, method, callback))
        elif isinstance(urlpattern, RegexURLResolver):
            endpoints += _get_endpoints(urlpattern.url_patterns, path)

    return endpoints
