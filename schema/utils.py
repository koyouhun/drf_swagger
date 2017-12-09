import importlib
from django.contrib.admindocs.views import simplify_regex
from rest_framework.views import APIView


def get_func_from_callback(method, callback):
    """
    Get function from callback
    :param callback: endpoint's callback (urlpattern's callback)
    :param method: get, post, ...
    :return: function
    """
    cls = getattr(callback, 'cls', None)
    actions = getattr(callback, 'actions', None)

    if cls is None:
        return None

    if actions is None:
        if callable(cls):
            return getattr(cls(), method.lower(), None)

    view_name = actions.get(method.lower(), None)

    if view_name is None:
        return None

    return getattr(cls, view_name, None)


def import_from_callback(callback):
    module = getattr(callback, '__module__', None)
    if module is None:
        cls = getattr(callback, '__cls__', None)
        module = getattr(cls, '__module__', None)
    try:
        lib = importlib.import_module('.'.join(module.split('.')[:-1]))
    except ImportError:
        return None
    return lib


def urlregex_to_path(path_regex):
    """
    Convert url regex to URI template string.
    """
    path = simplify_regex(path_regex)
    path = path.replace('<', '{').replace('>', '}')
    return path


def get_methods(callback):
    """
    Return a list of the valid HTTP methods for this endpoint.
    """
    if hasattr(callback, 'actions'):
        return [method.upper() for method in callback.actions.keys()]

    return [
        method for method in
        callback.cls().allowed_methods if method not in ('OPTIONS', 'HEAD')
    ]


def is_rest_framework_view(callback):
    cls = getattr(callback, 'cls', None)
    return cls is not None and issubclass(cls, APIView)
