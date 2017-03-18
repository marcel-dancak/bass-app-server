from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse


def user_passes_test(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    returning HTTP status code 401 otherwise. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponse("Login Required", status=401)
        return _wrapped_view
    return decorator

def login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated
    )
    if function:
        return actual_decorator(function)
    return actual_decorator