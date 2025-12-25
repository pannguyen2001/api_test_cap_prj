import json
import datetime
import pandas as pd
from typing import Dict
from string import Template
from requests import Response, get, post , put, patch, delete
from .test_case_setup import test_case_setup
from configs.constants import FILE_TYPE, FILETYPE, ROLE, APIMETHOD, VN_TIME_ZONE, DATETIMEFORMAT
from helpers import logger, logger_wrapper
# from common import User
from common.common_setup import admin, student, teacher



error_message: Dict = {
    "key_not_in_list": Template("[FAILED] Key: '${expected}' is not in list of keys: ${actual}."),
    "value_not_in_list": Template("[FAILED] Value: '${actual}' is not in list of values: ${expected}."),
    "status_code_not_equal": Template("[FAILED] Status code is not equal. Expected: ${expected}, Actual: ${actual}."),
    "value_not_equal": Template("[FAILED] Value is not equal. Expected: '${expected}', Actual: '${actual}'."),

}
passed_message: Dict = {
    "key_in_list": Template("[PASSED] Key: '${expected}' is in list of keys: ${actual}."),
    "value_in_list": Template("[PASSED] Value: '${actual}' is in list of values: '${expected}'."),
    "status_code_equal": Template("[PASSED] Status code is equal. Expected: ${expected}, Actual: ${actual}."),
    "value_equal": Template("[PASSED] Value is equal. Expected: '${expected}', Actual: '${actual}'."),
}

@logger_wrapper
def run_case(
    file_path: str = "",
    file_type: FILE_TYPE = FILETYPE.TEXT.value,
    pre_data: Dict = None,
    ) -> None:
    df_test_case: pd.DataFrame = test_case_setup(file_path, file_type, pre_data)
    if df_test_case.empty:
        logger.warning("Setup test case failed. End run case.")
        return

    df_test_case["result"] = [None for i in range(df_test_case.shape[0])]
    df_test_case["detail"] = [list() for i in range(df_test_case.shape[0])]
    df_test_case["datetime"] = datetime.datetime.now().astimezone(VN_TIME_ZONE).strftime(DATETIMEFORMAT.DATETIME.value)

    for index, row in df_test_case.iterrows():
        logger.info(f"Run case: {row['case_no']} - {row['description']}")
        if row["role"] == ROLE.ADMIN.value:
            user = admin
        elif row["role"] == ROLE.STUDENT.value:
            user = student
        elif row["role"] == ROLE.TEACHER.value:
            user = teacher

        res: Response = None
        header: Dict = user.client.get_header()
        request_body: any = row["request_body"]
        logger.info(f"Request body:\n{json.dumps(request_body, indent=4)}")
        if row["method"] == APIMETHOD.GET.value:
            res = get(row["api"],headers=header,json=row["request_body"])
        elif row["method"] == APIMETHOD.POST.value:
            res = post(row["api"],headers=header,json=row["request_body"])
        elif row["method"] == APIMETHOD.PUT.value:
            res = put(row["api"],headers=header,json=row["request_body"])
        elif row["method"] == APIMETHOD.PATCH.value:
            res = patch(row["api"],headers=header,json=row["request_body"])
        elif row["method"] == APIMETHOD.DELETE.value:
            res = delete(row["api"],headers=header,json=row["request_body"])
        # user.client.logout()
        logger.info(f"Response:\n{res.status_code}, {res.text}")

        status_code: int = res.status_code
        logger.info(f"Expected result: {row['expected_result']}")
        for key, value in row["expected_result"].items():
            logger.info(f"Key: {key}, Value: {value}")
            if key == "status_code":
                if status_code != value:
                    status_code_not_equal_error_message: str = error_message["status_code_not_equal"].substitute(expected=value, actual=status_code)
                    logger.error(status_code_not_equal_error_message)
                    row["detail"].append(status_code_not_equal_error_message)
                else:
                    logger.success(passed_message["status_code_equal"].substitute(expected=value, actual=status_code))
            elif status_code >= 400:
                logger.error(f"Request error:\nStatus:{res.status_code}.\nText:{res.text}")
                continue
            else:
                data = res.json()
                if not data:
                    logger.error("No data found")
                    continue

                if isinstance(data, list):
                    key_list: list = data[0].keys()
                    actual_detail: list = [i.get(key) for i in data]
                elif isinstance(data, dict):
                    key_list: list = data.keys()
                if key not in key_list:
                    key_not_in_list_error_message: str = error_message["key_not_in_list"].substitute(expected=key, actual=key_list)
                    logger.error(key_not_in_list_error_message)
                    row["detail"].append(key_not_in_list_error_message)
                else:
                    logger.success(passed_message["key_in_list"].substitute(expected=key, actual=key_list))

                if isinstance(data, list):
                    actual_detail: list = [i.get(key) for i in data]
                    if value not in actual_detail:
                        value_not_in_list_error_message: str = error_message["value_not_in_list"].substitute(expected=value, actual=actual_detail)
                        logger.error(value_not_in_list_error_message)
                        row["detail"].append(value_not_in_list_error_message)
                    else:
                        logger.success(passed_message["value_in_list"].substitute(expected=value, actual=actual_detail))

                elif isinstance(data, dict):
                    if data.get(key) != value:
                        value_not_equal_error_message: str = error_message["value_not_equal"].substitute(expected=value, actual=data.get(key))
                        logger.error(value_not_equal_error_message)
                        row["detail"].append(value_not_equal_error_message)
                    else:
                        logger.success(passed_message["value_equal"].substitute(expected=value, actual=data.get(key)))


        logger.success(f"Done case: {row['case_no']} - {row['description']}")
    df_test_case["result"] = df_test_case["detail"].map(lambda x: "Failed" if x else "Passed")
    df_test_case["detail"] = df_test_case["detail"].map(lambda x: "\n".join(x))

    logger.success("All test cases are done.")
    return df_test_case