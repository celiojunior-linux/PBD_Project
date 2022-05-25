from django.contrib.auth import get_user as get_employee
from django.shortcuts import resolve_url, redirect
from django.utils.functional import SimpleLazyObject


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
