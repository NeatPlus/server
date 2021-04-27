import random
import string


def random_N_digit_number(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def random_N_length_string(n):
    return "".join(random.choice(string.ascii_lowercase) for i in range(16))
