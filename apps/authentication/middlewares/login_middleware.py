from django.conf import settings
from django.contrib.auth import _get_user_session_key, BACKEND_SESSION_KEY, load_backend, HASH_SESSION_KEY, logout
from django.shortcuts import resolve_url, redirect
from django.utils.crypto import constant_time_compare
from django.utils.functional import SimpleLazyObject


def get_employee(request):
    from django.contrib.auth.models import AnonymousUser

    employee = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            employee = backend.get_user(user_id)
            # Verify the session
            if hasattr(employee, "get_session_auth_hash"):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash, employee.get_session_auth_hash()
                )
                if not session_hash_verified:
                    request.session.flush()
                    employee = None
    return employee or AnonymousUser()


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = get_employee(request)
    return request._cached_user


class EmployeeLoginMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = resolve_url("authentication:login-view")
        request.user = SimpleLazyObject(lambda: get_user(request))
        if not request.user.is_authenticated and request.path != login_url:
            response = redirect(login_url)
            response["location"] += f"?next={request.path}"
            return response
        return self.get_response(request)
