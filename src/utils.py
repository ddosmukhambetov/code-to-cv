import random
import string

from slugify import slugify


def generate_slug_with_random_chars(value: str):
    random_chars = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f'{slugify(value)}-{random_chars}'
