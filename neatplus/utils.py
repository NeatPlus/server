import secrets
import string

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

RANDOM_STRING_CHARS = string.ascii_letters + string.digits


def gen_random_number(length):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return secrets.choice(range(range_start, range_end))


def gen_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for _ in range(length))


def gen_random_password(
    length=12,
    allowed_chars="abcdefghjkmnpqrstuvwxyz" + "ABCDEFGHJKLMNPQRSTUVWXYZ" + "23456789",
    user=None,
) -> str:
    random_password = gen_random_string(length, allowed_chars)
    try:
        validate_password(random_password, user)
        return random_password
    except ValidationError as _err:
        return gen_random_password(length=length, allowed_chars=allowed_chars)
