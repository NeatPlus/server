import secrets
import string

RANDOM_STRING_CHARS = string.ascii_letters + string.digits


def gen_random_number(length):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return secrets.choice(range(range_start, range_end))


def gen_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for _ in range(length))
