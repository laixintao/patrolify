import shutil

import logging
import glob
from typing import List
from .globals import g
from .consts import RESULT_FILE_NAME
import dataclasses, json
from redis.lock import Lock

logger = logging.getLogger(__name__)
MAX_LATEST_CHECK_ID_RECORDING = 100


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclasses.dataclass()
class MainResult:
    passed: List[str] = dataclasses.field(default_factory=list)
    not_passed: List[str] = dataclasses.field(default_factory=list)
    failed: List[str] = dataclasses.field(default_factory=list)


def generate_report(check_name, check_id):
    logger.info("Start to generate reports for %s check_id=%s", check_name, check_id)
    check_directory = g.result_dir(check_name, check_id)
    report_directory = g.report_dir(check_name, check_id)

    main_reuslt = MainResult()
    for file in glob.glob(str(check_directory / "*-*-*-*-*.json")):
        logger.debug("Parse result %s...", file)
        with open(file, "r") as f:
            result = json.load(f)

        if not result["run_success"]:
            main_reuslt.failed.append(result["job_id"])

        if result["check_pass"]:
            main_reuslt.passed.append(result["job_id"])
        else:
            main_reuslt.not_passed.append(result["job_id"])

    main_result_location = check_directory / RESULT_FILE_NAME
    with open(main_result_location, "w") as f:
        json.dump(main_reuslt, f, cls=EnhancedJSONEncoder)

    shutil.move(check_directory, report_directory)

    logger.info("result has been writen to %s", report_directory)
    update_latest_check(check_name, check_id)


def update_latest_check(check_name, check_id):
    """
    write the check_id into the latest check file
    """
    lock = Lock(g.redis, "reporter:lock:update_latest_check_file")
    with lock:
        old_check_ids = get_latest_check_ids(check_name)

        existing_records = len(old_check_ids)
        if existing_records >= MAX_LATEST_CHECK_ID_RECORDING:
            pass
        else:
            start = existing_records - MAX_LATEST_CHECK_ID_RECORDING + 1
            old_check_ids = old_check_ids[start:]

        old_check_ids.append(f"{check_id}\n")
        logger.info("old check ids: %s", old_check_ids)
        with open(g.latest_check_ids_file(check_name), "w") as f:
            f.writelines(old_check_ids)


def get_latest_check_ids(check_name) -> List[str]:
    if not g.latest_check_ids_file(check_name).exists():
        return []
    with open(g.latest_check_ids_file(check_name), "r") as f:
        old_check_ids = f.readlines()
    return old_check_ids
