from typing import Dict
from requests import Response

def validate_response(funct_name: str = "", res: Response = None, validate_conditions: Dict = None):
    # if not validate_conditions:
    #     validate_conditions = {"code": 200, "status": 0}
    if res.status_code >= 400:
        raise Exception(f"[{funct_name}] Request error:\nStatus:{res.status_code}. Text:{res.text}")
        return None
    res = res.json()
    # if validate_conditions:
    #     for key, value in validate_conditions.items():
    #         if res[key] != value:
    #             raise Exception(f"[{funct_name}] Request error: {res}")

    return res