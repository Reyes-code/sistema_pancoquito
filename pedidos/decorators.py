# core/auth_utils.py
from functools import wraps
from django.core.exceptions import PermissionDenied

def group_required(*group_names, allow_superuser=True):
    """

    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            u = request.user
            if not u.is_authenticated:

                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())

            if allow_superuser and u.is_superuser:
                return view_func(request, *args, **kwargs)

            if u.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)

            raise PermissionDenied 
        return _wrapped
    return decorator
