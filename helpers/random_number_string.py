import random

def random_number_string(length: int = 10) -> str:
    random_num: int = random.randint(1 * (10 ** (length - 1)), 1 * (10 ** length) - 1)
    return str(random_num)
