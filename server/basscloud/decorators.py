from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.core.cache import cache

from basscloud.cache import version_key, index_key


def login_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        response = HttpResponse("", status=401)
        response['Content-Length'] = 0
        return response
    return _wrapped_view


def view_cache(func=None, timeout=60):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            key = request.path
            resp = cache.get(key)
            if resp:
                # print('loading from cache:', key)
                return resp

            resp = view_func(request, *args, **kwargs)
            # print('writting to cache', key)
            cache.set(key, resp, timeout)
            return resp
        return _wrapped_view

    if func:
        return decorator(func)
    return decorator


def indexed_cache(func=None, excluded=('page',), timeout=60):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            use_cache = set(request.GET.keys()).issubset(set(excluded))
            # print('use_cache:', use_cache)
            if use_cache:
                version = request.META['QUERY_STRING']
                key = version_key(request.path, version)
                resp = cache.get(key)
                if resp:
                    # print('loading from cache:', key)
                    return resp

            resp = view_func(request, *args, **kwargs)
            if use_cache:
                # print('writting to cache', key)
                cache.set(key, resp, timeout)
                index = cache.get(index_key(request.path), [])
                if version not in index:
                    index.append(version)
                    # print('updating index:', index)
                    cache.set(index_key(request.path), index)

            return resp
        return _wrapped_view

    if func:
        return decorator(func)
    return decorator



def clear_cache(view_func):
    """Clear cache after successful POST request."""
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if request.method == 'POST' and response.status_code == 200:
            # print('CLEAR CACHE')
            cache.clear()
        return response
    return _wrapped_view