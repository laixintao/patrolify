import dataclasses
import glob
import json
import json
import logging
import shutil
from typing import Dict, List

from redis.lock import Lock

from .consts import RESULT_FILE_NAME
from .globals import g

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
    all_passed: bool = True
    job_info: Dict[str, Dict] = dataclasses.field(default_factory=dict)
    start_job_id: str | None = None


def generate_report(check_name, check_id):
    logger.info("Start to generate reports for %s check_id=%s", check_name, check_id)
    check_directory = g.result_dir(check_name, check_id)
    report_directory = g.report_dir(check_name, check_id)

    main_result = MainResult()

    for file in glob.glob(str(check_directory / "*-*-*-*-*.json")):
        logger.debug("Parse result %s...", file)
        with open(file, "r") as f:
            result = json.load(f)

        # save job information
        job_id = result["job_id"]
        target_name = result["target"]
        job_info = main_result.job_info.setdefault(job_id, {})
        job_info["target"] = target_name
        job_info["run_success"] = result['run_success']
        job_info["check_pass"] = result['check_pass']
        job_info.setdefault("child_job_ids", [])

        # save job's relation
        parent_id = result["parent_target_id"]
        if parent_id is None:
            main_result.start_job_id = job_id
        else:
            parent = main_result.job_info.setdefault(parent_id, {})
            parent.setdefault("child_job_ids", []).append(job_id)

        # save result
        if not result["run_success"]:
            main_result.failed.append(result["job_id"])
            main_result.all_passed = False
            continue

        if result["check_pass"]:
            main_result.passed.append(result["job_id"])
        else:
            main_result.all_passed = False
            main_result.not_passed.append(result["job_id"])

    check_directory.mkdir(parents=True, exist_ok=True)

    main_result_location = check_directory / RESULT_FILE_NAME
    with open(main_result_location, "w") as f:
        json.dump(main_result, f, cls=EnhancedJSONEncoder)

    shutil.move(check_directory, report_directory)

    logger.info("result has been writen to %s", report_directory)
    update_latest_check(check_name, check_id)


def update_latest_check(check_name, check_id):
    """
    write the check_id into the latest check file
    """
    lock = Lock(g.redis, "patrolify:lock:update_latest_check_file")
    with lock:
        old_check_ids = get_latest_check_ids(check_name)

        existing_records = len(old_check_ids)
        if existing_records >= MAX_LATEST_CHECK_ID_RECORDING:
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


def get_check_report(check_name, check_id):
    with open(g.report_dir(check_name, check_id) / RESULT_FILE_NAME) as f:
        report_result = json.load(f)

    return report_result


def get_result_by_job_id(check_name, check_id, job_id):
    with open(g.report_dir(check_name, check_id) / f"{job_id}.json") as f:
        report_result = json.load(f)

    return report_result



def store_check_result(result, target, check_name, check_id, job_id, parent_id):
    data = {
        "job_id": job_id,
        "target": target,
        "parent_target_id": parent_id,
        "run_success": None,
        "check_pass": None,
        "reason": None,
    }

    if result is None:
        pass
    elif isinstance(result, tuple):
        boolresult, reason = result

        data.update(
            {
                "run_success": True,
                "check_pass": boolresult,
                "reason": reason,
            }
        )

    result_dir = g.result_dir(check_name, check_id)
    result_dir.mkdir(parents=True, exist_ok=True)
    with open(str(result_dir / job_id) + ".json", "w") as f:
        json.dump(data, f)
        logger.info("Job result has been saved to %s", f)
