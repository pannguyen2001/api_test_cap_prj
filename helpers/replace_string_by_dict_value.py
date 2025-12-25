from typing import Dict

def replace_string_by_dict_value(string: str = "", replace_dict: Dict = {}) -> str:
    for key, value in replace_dict.items():
        string = string.replace("{" + key + "}", value)
        string = string.replace("{[" + key + "]}", value)
    return string