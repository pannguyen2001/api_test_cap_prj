import json
import pandas as pd
from typing import Dict
from helpers import logger
from case_setup import role_case_setup, account_case_setup, run_case
from configs.constants import report_file_path, TEST_CASE_FILE_PATH, MODULETEST
from common.common_setup import admin, teacher, student

logger.info(f"{' Start testing ':=^50}")

# check env and package: cpu, storage, ...

# Define module test
module_test: str = MODULETEST.ACCOUNT.value

# create predata
# role_pre_data: Dict = role_case_setup()
account_pre_data: Dict = account_case_setup()

# test case setup
# run test case
df_run_case: pd.DataFrame = run_case(
    file_path=TEST_CASE_FILE_PATH, file_type="excel", pre_data=account_pre_data
)

df_final_result: pd.DataFrame = df_run_case[
    ["result", "case_no", "expected_result", "detail", "datetime"]
]
if not df_final_result.empty:
    df_final_result.index = df_final_result.index + 1
    df_final_result = df_final_result.reset_index()
    total_cases: int = df_final_result.shape[0]
    passed_case: int = df_final_result[df_final_result["result"] == "Passed"].shape[0]
    failed_case: int = df_final_result[df_final_result["result"] == "Failed"].shape[0]
    logger.info(f"Total cases: {total_cases}")
    logger.info(f"Pass cases: {passed_case}")
    logger.info(f"Failed cases: {failed_case}")
    pretty_detail_result: str = json.dumps(
        df_final_result.to_dict(orient="records"), indent=4
    )
    logger.info(f"Detail result:\n{pretty_detail_result}")
    # save report to excel file
    if not df_final_result[df_final_result["result"] == "Failed"].empty:
        df_final_result[df_final_result["result"] == "Failed"].to_excel(
            report_file_path,
            sheet_name=module_test,
            index=False
        )
        logger.success(f"Report saved to '{report_file_path}'.")

admin.client.logout()
student.client.logout()
teacher.client.logout()
logger.success(f"{' End testing ':=^50}")
