import json
from typing import Dict

def dict_to_str(dict_input: Dict = None) -> str:
    return json.dumps(dict_input, separators=(",", ":"))

