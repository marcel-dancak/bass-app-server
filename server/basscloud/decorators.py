from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse, HttpResponseForbidden
from django.core.cache import cache


def login_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view


def conditional_cache(func=None, excluded=tuple(), timeout=60):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            use_cache = set(request.GET.keys()).issubset(set(excluded))
            if use_cache:
                cache_key = request.path+'?'+request.META['QUERY_STRING']
                resp = cache.get(cache_key)
                if resp:
                    print('loading from cache')
                    return resp

            resp = view_func(request, *args, **kwargs)
            if use_cache:
                print('writting to cache')
                cache.set(cache_key, resp, timeout)
            return resp
        return _wrapped_view

    if func:
        return decorator(func)
    return decorator