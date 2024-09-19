from threading import local

from Users.models import VitalizeUser

_user = local()


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        return response


def get_current_user() -> VitalizeUser | None:
    return getattr(_user, 'value', None)
