import string
import random

def random_string(length: int = 10, include_special_char: bool = False, inclide_digit: bool = False, exculde: str = "") -> str:
    string_pool = string.ascii_letters
    if include_special_char:
        string_pool += string.punctuation
    if inclide_digit:
        string_pool += string.digits
    if exculde:
        for char in exculde:
            string_pool = string_pool.replace(char, "")
    return "".join(random.choices(string_pool, k=length))