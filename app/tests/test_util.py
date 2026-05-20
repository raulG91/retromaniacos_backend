import random
import string

def create_random_email() -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"

