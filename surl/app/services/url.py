import random
import string

ALPHABET: str = string.ascii_lowercase + string.digits


def gen_short_uuid() -> str:
    return "".join(random.choices(ALPHABET, k=8))
