import json
import pandas as pd
from .logger import logger
from .logger_wrapper import logger_wrapper
from configs.constants import BASE_URL

@logger_wrapper
def print_test_result(df_final_result: pd.DataFrame = None) -> None:
    df_final_result["api"] = df_final_result["api"].astype(str).str.replace(BASE_URL, "")
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