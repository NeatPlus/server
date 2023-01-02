from defender import config as defender_config
from defender import utils as defender_utils
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationDefender(JWTAuthentication):
    def authenticate(self, request):
        response = super().authenticate(request)
        if response is None:
            return None

        block_detail_message = _(
            "You have attempted to login {failure_limit} times with no success. Wait {cooloff_time_seconds} seconds to re login"
        ).format(
            failure_limit=defender_config.FAILURE_LIMIT,
            cooloff_time_seconds=defender_config.COOLOFF_TIME,
        )
        block_exception = exceptions.AuthenticationFailed(block_detail_message)

        if defender_utils.is_already_locked(request, username=response[0].username):
            raise block_exception

        defender_utils.add_login_attempt_to_db(
            request,
            login_valid=True,
            username=response[0].username,
        )
        user_not_blocked = defender_utils.check_request(
            request,
            login_unsuccessful=False,
            username=response[0].username,
        )
        if user_not_blocked:
            return response
        else:
            raise block_exception


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass
