from django.http import HttpRequest
from django.views import View

from .services import InvalidTokenError, get_authenticated_user
from .utils import error_response


class AuthenticatedMixin(View):
    user = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            self.user = get_authenticated_user(request)
        except InvalidTokenError as exc:
            return error_response(str(exc), status=401)

        if self.user is None:
            return error_response("Authentication credentials were not provided.", status=401)

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AuthenticatedMixin):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            self.user = get_authenticated_user(request)
        except InvalidTokenError as exc:
            return error_response(str(exc), status=401)

        if self.user is None:
            return error_response("Authentication credentials were not provided.", status=401)

        if self.user.role != self.user.ROLE_ADMIN:
            return error_response("Admin access is required.", status=403)

        return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)
