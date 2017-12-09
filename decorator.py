from functools import wraps


def drf_request(request):
    """
    Add view function's swagger request info
    """
    def wrapper(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)
        wrapped_view.drf_request = request
        return wraps(view_func)(wrapped_view)
    return wrapper


def drf_response(response):
    """
    Add view function's swagger response info
    """
    def wrapper(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)
        wrapped_view.drf_response = response
        return wraps(view_func)(wrapped_view)
    return wrapper
